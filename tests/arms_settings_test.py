import json
import os

from scylla_arms.config import ArmsSettings, inject_persistent_models


class SampleArmsSettings(ArmsSettings):
    foo: int = 1
    bar: str = "abc"


class TestArmsSettings:
    def test_arms_settings_are_persisted_upon_creation(self):
        SampleArmsSettings(foo=2, bar="test")
        assert os.path.exists(
            "SampleArmsSettings.json"
        ), "SampleArmsSettings.json was not created upon settings creation"

    def test_arms_settings_are_persisted_upon_modification(self):
        settings = SampleArmsSettings(foo=2, bar="test")
        settings.foo = 4
        settings.bar = "test change"
        with open("SampleArmsSettings.json") as f:
            loaded_settings = json.load(f)
        assert settings.foo == loaded_settings["foo"]
        assert settings.bar == loaded_settings["bar"]

    def test_arms_settings_can_be_loaded_from_file(self):
        SampleArmsSettings(foo=3, bar="test 2")
        settings = SampleArmsSettings.load()
        assert settings.foo == 3
        assert settings.bar == "test 2"


class TestInjectPersistedModelDecorator:
    def test_inject_persisted_model_decorator_injects_instance_of_arms_settings(self):
        @inject_persistent_models
        def test_function(ctx, settings: SampleArmsSettings):
            assert settings.foo == 2
            assert settings.bar == "test"

        SampleArmsSettings(foo=2, bar="test")
        test_function(ctx={})

    def test_inject_persisted_model_decorator_passes_all_provided_arguments(self):
        @inject_persistent_models
        def test_function(ctx, settings: SampleArmsSettings, bar: int):
            assert bar == 88

        SampleArmsSettings(foo=2, bar="test")
        test_function(ctx={}, bar=88)
