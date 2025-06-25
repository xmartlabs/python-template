import asyncio
import inspect
from typing import Dict, Type

from ptpython.repl import embed

from src import models
from src.core.config import settings
from src.core.database import SQLBase, async_session_generator


def _get_models() -> Dict[str, Type[SQLBase]]:
    models_dict: Dict[str, Type[SQLBase]] = {}
    for name, obj in inspect.getmembers(models):
        if inspect.isclass(obj) and issubclass(obj, SQLBase):
            models_dict[name] = obj
    return models_dict


async def _start_shell_async() -> None:
    """Async shell function that properly handles the async session"""
    models = _get_models()
    async_session = async_session_generator()
    async with async_session() as session:
        locals = {"session": session, "settings": settings, **models}
        embed(locals=locals, history_filename=".ptpython-history")


def _start_shell() -> None:
    """Start the shell - wrapper to handle async context"""
    try:
        # Try to use existing event loop if available
        asyncio.get_running_loop()
        # If we're already in an async context, we can't use asyncio.run
        asyncio.create_task(_start_shell_async())
    except RuntimeError:
        # No event loop running, start new one
        asyncio.run(_start_shell_async())


if __name__ == "__main__":
    _start_shell()
