import asyncio
import os
from concurrent.futures import ThreadPoolExecutor

from tortoise import Tortoise, fields
from tortoise.models import Model

_async_executor = ThreadPoolExecutor(max_workers=4)


def run_async(coro):
    """Run an async coroutine from sync code, whether or not a loop is already running."""
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)
    else:
        return _async_executor.submit(asyncio.run, coro).result()

DATABASE_URL = os.environ["DATABASE_URL"]

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["database", "aerich.models"],
            "default_connection": "default",
        }
    },
}


class Conversation(Model):
    id = fields.IntField(pk=True)
    thread_id = fields.CharField(max_length=255, unique=True, index=True)
    title = fields.CharField(max_length=255, default="New Chat")
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "conversations"


class ChatMessage(Model):
    id = fields.IntField(pk=True)
    thread_id = fields.CharField(max_length=255, index=True)
    role = fields.CharField(max_length=32)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "chat_messages"


class LongTermMemory(Model):
    id = fields.IntField(pk=True)
    thread_id = fields.CharField(max_length=255, index=True)
    memory = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "long_term_memory"


async def init_db():
    # Schema is managed by Aerich migrations (see migrations/), not generated here.
    await Tortoise.init(config=TORTOISE_ORM)


async def close_db():
    await Tortoise.close_connections()


async def create_or_update_conversation(thread_id: str, first_message: str | None = None):
    conversation = await Conversation.filter(thread_id=thread_id).first()

    if not conversation:
        title = "New Chat"

        if first_message:
            title = first_message.strip()[:40]
            if len(first_message.strip()) > 40:
                title += "..."

        await Conversation.create(thread_id=thread_id, title=title)

    else:
        await conversation.save()


async def list_conversations():
    return await Conversation.all().order_by("-updated_at")


async def save_chat_message(thread_id: str, role: str, content: str):
    await ChatMessage.create(thread_id=thread_id, role=role, content=content)

    conversation = await Conversation.filter(thread_id=thread_id).first()

    if conversation:
        await conversation.save()


async def get_chat_history(thread_id: str):
    return await ChatMessage.filter(thread_id=thread_id).order_by("created_at")


async def save_memory(thread_id: str, memory: str):
    await LongTermMemory.create(thread_id=thread_id, memory=memory)

    return "Memory saved succesfully"


async def search_memory(thread_id: str, query: str):
    memories = (
        await LongTermMemory.filter(thread_id=thread_id)
        .order_by("-created_at")
        .limit(20)
    )

    if not memories:
        return "No saved memory found"

    return "\n".join([f"- {m.memory}" for m in memories])
