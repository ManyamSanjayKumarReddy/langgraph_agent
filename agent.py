import os

from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
from dotenv import load_dotenv

load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.postgres import PostgresSaver
from tools import tools

_checkpoint_pool = ConnectionPool(
    os.environ["DATABASE_URL"],
    min_size=1,
    max_size=10,
    kwargs={"autocommit": True, "prepare_threshold": 0, "row_factory": dict_row},
)

checkpointer = PostgresSaver(_checkpoint_pool)
checkpointer.setup()

## allow sepecific models to be used
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

ALLOWED_MODELS = {
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-2.5-flash-lite",
    "gemini-1.5-flash",
    "gemini-1.5-pro"
}


SYSTEM_PROMPT = """
You are a helpful Agentic AI assistant named CodeGPT similar to ChatGPT.

You can:
1. Answer normal questions.
2. Use tools when needed.
3. Search uploaded documents using the RAG tool.
4. Search the web for latest/current information using Tavily Search.
5. Remember important user information using the memory tool.
6. Recall memory when useful.
7. Use calculator for math.

Rules:
- If the user asks about latest news, current events, recent updates, today's information, current prices, current people, current versions, new releases, or anything time-sensitive, use Tavily Search.
- If the user asks about an uploaded document, use search_uploaded_documents.
- If the user asks you to remember something, use remember_this.
- If the user asks about previous preferences or saved facts, use recall_memory.
- Use calculator for math questions.
- When using web search, summarize clearly and mention that the answer is based on web search results.
- Be clear, helpful, and concise.
"""

def normalize_model_name(model_name : str  | None) -> str:
    """ 
    Validate selected model from frontend
    if model is missing from the allowed list set to default model
    """
    
    if not model_name or model_name not in ALLOWED_MODELS:
        return DEFAULT_MODEL
    
    model_name = model_name.strip().lower()

    return model_name

def build_agent(model_name:str):
    """
    Build one langgraph agent for the selected gemini model
    """
    
    selected_model = normalize_model_name(model_name)
    
    # initilize gemini llm
    llm = ChatGoogleGenerativeAI(
        model=selected_model,
        temperature=0.4,
        streaming=True
    )
    
    
    llm_with_tools = llm.bind_tools(tools)
    
    def chatbot_node(state: MessagesState):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
        
        response = llm_with_tools.invoke(messages)
        
        return {"messages": [response]}
    
    tool_node = ToolNode(tools)
    
    workflow = StateGraph(MessagesState)
    
    workflow.add_node("chatbot", chatbot_node)
    workflow.add_node("tools", tool_node)
    
    workflow.add_edge(START, "chatbot")
    workflow.add_conditional_edges("chatbot", tools_condition)
    workflow.add_edge("tools", "chatbot")
    
    return workflow.compile(checkpointer=checkpointer)
    
_AGENT_CACHE = {}

def get_agent(model_name:str | None = None):
    """ 
    Return cached langGraph agent for selected model
    If not created yet, create it once nd use it
    
    """
    
    selected_model = normalize_model_name(model_name)
    
    if selected_model not in _AGENT_CACHE:
        _AGENT_CACHE[selected_model] = build_agent(selected_model)
        
    return _AGENT_CACHE[selected_model]