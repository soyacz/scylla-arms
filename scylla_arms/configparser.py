import io
import configparser
import os
import re
from pathlib import PurePath


class JenkinsConfigParser:
    spacer_left: str
    delimiter: str
    spacer_right: str

    def __load(self):
        self._cfg = configparser.ConfigParser()
        self._cfg.optionxform = str
        self._cfg.read_file(io.StringIO(f"[global]\n{self._data}"))

    def __add(self, key, val):
        self._data += (
            f"{key}{self.spacer_left}{self.delimiter}{self.spacer_right}{val}\n"
        )
        self.__load()

    def __init__(self, filename, new_file=False):
        if isinstance(filename, PurePath):
            self._filename = str(filename)
        else:
            self._filename = filename
        if new_file and not os.path.exists(filename):
            with open(file=filename, mode="a", encoding="utf-8"):
                pass
        with open(file=filename, mode="r", encoding="utf-8") as file:
            self._data = file.read()
        self.__load()

    def get(self, key):
        return self._cfg.get("global", key)

    def has_option(self, key):
        return self._cfg.has_option("global", key)

    def set(self, key, val):
        if not self.has_option(key):
            self.__add(key, val)
            return
        self._data = re.sub(
            f"^{key}{self.spacer_left}{self.delimiter}{self.spacer_right}[^\n]*$",
            f"{key}{self.spacer_left}{self.delimiter}{self.spacer_right}{val}",
            self._data,
            flags=re.MULTILINE,
        )
        self.__load()

    def commit(self):
        with open(file=self._filename, mode="w", encoding="utf-8") as file:
            file.write(self._data)


class PropertiesParser(JenkinsConfigParser):
    spacer_left: str = ""
    delimiter: str = "="
    spacer_right: str = ""


class BuildMetadataParser(JenkinsConfigParser):
    spacer_left: str = ""
    delimiter: str = ":"
    spacer_right: str = " "
