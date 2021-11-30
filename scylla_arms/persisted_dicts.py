import json
import os
from collections.abc import MutableMapping


class FilePersistedDotDict(MutableMapping):
    """Dictionary that is saved to a file whenever attributes are set or deleted.
    dot.notation access to dictionary attributes.
    Init kwargs are dict defaults"""

    def __init__(self, persist_file_path, *args, **kwargs):
        self._store = {}
        self._persist_file_path = persist_file_path
        if os.path.exists(self._persist_file_path):
            with open(file=self._persist_file_path, mode="r", encoding="utf-8") as persist_file:
                kwargs.update(json.load(persist_file))
        self.update(dict(*args, **kwargs))  # use the free update to set keys
        self._persist()

    def __copy__(self):
        return self

    def __getitem__(self, key):
        return self._store[key]

    def __setitem__(self, key, value):
        self._store[key] = value
        self._persist()

    def __getattr__(self, item):
        try:
            return self._store[item]
        except KeyError as error:
            raise AttributeError(item) from error

    def __setattr__(self, key, value):
        if key in ("_store", "_persist_file_path"):
            super().__setattr__(key, value)
        else:
            self._store[key] = value
            self._persist()

    def __delitem__(self, key):
        del self._store[key]
        self._persist()

    def __delattr__(self, key):
        del self._store[key]
        self._persist()

    def __iter__(self):
        return iter(self._store)

    def __len__(self):
        return len(self._store)

    def _persist(self):
        with open(file=self._persist_file_path, mode="w", encoding="utf-8") as persist_file:
            persist_file.write(json.dumps(self._store, indent=2))

    def dict(self):
        return self._store
