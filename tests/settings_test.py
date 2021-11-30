# pylint: disable=disallowed-name
import os
from typing import List

from scylla_arms.config import ArmsSettings


class ArmsSettingsForTest(ArmsSettings):
    foo: str
    bar: int
    li: List[str]


class TestPersistentSettings:
    @staticmethod
    def test_settings_can_be_override_by_jenkins_params_env_var():
        os.environ["JENKINS_PARAMS"] = '[foo: im_foo, bar: 888, li:["val1", "val2"], cos: 44]'

        settings = ArmsSettingsForTest()
        assert settings.foo == "im_foo"
        assert settings.bar == 888
        assert settings.li == ["val1", "val2"]

    @staticmethod
    def test_settings_can_be_override_by_env_file():
        with open(file=".env", mode="w", encoding="utf-8") as file:
            file.writelines([
                "foo=im_foo",
                "bar=88",
                "li=[val1, val2]"
            ])

        settings = ArmsSettingsForTest()
        assert settings.foo == "im_foo"
        assert settings.bar == 888
        assert settings.li == ["val1", "val2"]
