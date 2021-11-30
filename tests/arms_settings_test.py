# pylint: disable=blacklisted-name
import json
import os

from scylla_arms.config import ArmsSettings, inject_persistent_models


class SampleArmsSettings(ArmsSettings):
    foo: int = 1
    bar: str = "abc"


class TestArmsSettings:
    @staticmethod
    def test_arms_settings_are_persisted_upon_creation():
        SampleArmsSettings(foo=2, bar="test")
        assert os.path.exists(
            "SampleArmsSettings.json"
        ), "SampleArmsSettings.json was not created upon settings creation"

    @staticmethod
    def test_arms_settings_are_persisted_upon_modification():
        settings = SampleArmsSettings(foo=2, bar="test")
        settings.foo = 4
        settings.bar = "test change"
        with open(file="SampleArmsSettings.json", mode="r", encoding="utf-8") as file:
            loaded_settings = json.load(file)
        assert settings.foo == loaded_settings["foo"]
        assert settings.bar == loaded_settings["bar"]

    @staticmethod
    def test_arms_settings_can_be_loaded_from_file():
        SampleArmsSettings(foo=3, bar="test 2")
        settings = SampleArmsSettings.load()
        assert settings.foo == 3
        assert settings.bar == "test 2"


class TestInjectPersistedModelDecorator:
    @staticmethod
    def test_inject_persisted_model_decorator_injects_instance_of_arms_settings():
        @inject_persistent_models
        def _test_function(ctx, settings: SampleArmsSettings):  # pylint: disable=unused-argument
            assert settings.foo == 2
            assert settings.bar == "test"

        SampleArmsSettings(foo=2, bar="test")
        _test_function(ctx={})  # pylint: disable=no-value-for-parameter

    @staticmethod
    def test_inject_persisted_model_decorator_passes_all_provided_arguments():
        @inject_persistent_models
        def _test_function(ctx, bar: int):  # pylint: disable=unused-argument
            assert bar == 88

        SampleArmsSettings(foo=2, bar="test")
        _test_function(ctx={}, bar=88)
