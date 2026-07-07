import math
from dotenv import load_dotenv

load_dotenv()

from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from database import save_memory, search_memory
from rag import retrieve_from_rag


CURRENT_THREAD_ID = "default"

def set_current_thread_id(thread_id: str):
    global CURRENT_THREAD_ID
    CURRENT_THREAD_ID = thread_id

web_search = TavilySearch(
    max_results = 3,
    topic="general",
    search_depth = "advanced"
)

@tool
def calculator(expression: str) -> str:
    """
    A tool that evaluates a mathematical expression and returns the result.
    """
    
    try:
        allowed = {
            "math": math,
            "abs": abs,
            "round": round,
            "min" : min,
            "max": max,
            "sum" : sum
        }
        
        result = eval(expression, {"__builtins__": {}}, allowed)
        return str(result)
    except Exception as e:
        return f"Calculation Error: {str(e)}"

@tool
def remember_this(memory:str) -> str:
    """
    Save an important user preferences or fact into long term memory
    use this when user asks you to remember something
    """
    
    return save_memory(
        thread_id=CURRENT_THREAD_ID,
        memory=memory
    )
    
@tool
def recall_memory(query: str) -> str:
    """ Recall saved long term memories about the user or this conversation"""
    
    return search_memory(
        thread_id=CURRENT_THREAD_ID,
        query=query
    )
    
@tool
def search_uploaded_documents(query:str) -> str:
    """ 
    
    Search uploaded documents for relevant information
    Use this when the user asks about uploaded PDF's, DOCX, TXT , notes ,files or documents
    
    """
    
    return retrieve_from_rag(
        query=query,
        thread_id=CURRENT_THREAD_ID
    )
    
    
tools = [
    calculator,
    search_uploaded_documents,
    remember_this,
    recall_memory,
    web_search
]