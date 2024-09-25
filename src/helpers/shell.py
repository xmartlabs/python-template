import inspect
from typing import Dict, Type

from ptpython.repl import embed

from src import models
from src.core.config import settings
from src.core.database import SessionLocal, SQLBase


def _get_models() -> Dict[str, Type[SQLBase]]:
    models_dict: Dict[str, Type[SQLBase]] = {}
    for name, obj in inspect.getmembers(models):
        if inspect.isclass(obj) and issubclass(obj, SQLBase):
            models_dict[name] = obj
    return models_dict


def _start_shell() -> None:
    models = _get_models()
    with SessionLocal() as session:
        locals = {"session": session, "settings": settings, **models}
        embed(locals=locals, history_filename=".ptpython-history")


if __name__ == "__main__":
    _start_shell()
