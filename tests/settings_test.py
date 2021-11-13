import os
from typing import List

from scylla_arms.config import ArmsSettings


class TestPersistentSettings:
    def test_settings_can_be_override_by_jenkins_params_env_var(self):
        os.environ[
            "JENKINS_PARAMS"
        ] = '[foo: im_foo, bar: 888, li:["val1", "val2"], cos: 44]'

        class TestArmsSettings(ArmsSettings):
            foo: str
            bar: int
            li: List[str]

        settings = TestArmsSettings()
        assert settings.foo == "im_foo"
        assert settings.bar == 888
        assert settings.li == ["val1", "val2"]

    def test_settings_can_be_override_by_env_file(self):
        with open(".env", "w") as f:
            f.write("foo=im_foo\n")
            f.write("bar=888\n")
            f.write("li=[val1, val2]")

        class TestArmsSettings(ArmsSettings):
            foo: str
            bar: int
            li: List[str]

        settings = TestArmsSettings()
        assert settings.foo == "im_foo"
        assert settings.bar == 888
        assert settings.li == ["val1", "val2"]
