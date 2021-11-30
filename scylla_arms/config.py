from __future__ import annotations

import json
import os
import re
from functools import wraps
from typing import Dict, Any, Tuple
from pydantic import BaseSettings
from pydantic import BaseModel
from pydantic.env_settings import SettingsSourceCallable


def jenkins_params_settings_source(settings: BaseSettings) -> Dict[str, Any]:  # pylint: disable=unused-argument
    """
    A simple settings source that loads variables from a JSON file
    at the project's root.

    Here we happen to choose to use the `env_file_encoding` from Config
    when reading `config.json`
    """
    parsed_params = {}
    if raw_jenkins_params := os.getenv("JENKINS_PARAMS"):
        raw_jenkins_params = raw_jenkins_params[1:-1]
        scalar_params_patt = re.compile(r"(\w+):([^,]*)")
        for key, value in scalar_params_patt.findall(raw_jenkins_params):
            parsed_params[key] = value.strip()
        list_params_patt = re.compile(r"(\w+):(\[[^]]+\])")
        for key, value in list_params_patt.findall(raw_jenkins_params):
            parsed_params[key] = json.loads(value)
    return parsed_params


class PersistentModel(BaseModel):
    @classmethod
    def load(cls) -> PersistentModel:
        f_name = f"{cls.__name__}.json"
        if not os.path.exists(f_name):
            raise FileNotFoundError(f"The file '{f_name}' not exits")
        with open(file=f_name, mode="r", encoding="utf-8") as file:
            data = json.load(file)
        return cls(**data)

    def save(self) -> None:
        with open(file=f"{self.__class__.__name__}.json", mode="w", encoding="utf-8") as file:
            file.write(self.json(indent=2))

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self.save()

    def __setattr__(self, key: Any, value: Any) -> None:
        super().__setattr__(key, value)
        self.save()


class ArmsSettings(BaseSettings, PersistentModel):
    """Pydantic base settings class with ability to use JENKINS_PARAMS env variable as values source.
    It also is persisted to a file upon creation/update for further load.

    Use `incject_persistent_models` decorator to automatically inject instance of this class loaded from file"""

    class Config:
        env_file_encoding = "utf-8"
        extra = "ignore"

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ) -> Tuple[SettingsSourceCallable, ...]:
            return (
                init_settings,
                jenkins_params_settings_source,
                env_settings,
                file_secret_settings,
            )


def inject_persistent_models(func):
    """loads `PersistentModel` function arguments from persistent storage and injects its instance"""

    @wraps(func)
    def inner(ctx, *args, **kwargs):
        loaded = {}
        for arg, ann in func.__annotations__.items():
            if hasattr(ann, "load"):
                loaded[arg] = ann.load()
        loaded.update(**kwargs)
        return func(ctx, *args, **loaded)

    return inner
