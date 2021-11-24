# pylint: disable=blacklisted-name
import pathlib
from enum import Enum

from pydantic import BaseModel

from scylla_arms.config import PersistentModel


class EnumForTest(Enum):
    foo: str = "foo"
    bar: str = "bar"


class PydanticModel(BaseModel):
    foo: str = "foo"
    bar: bool = True


class PersistedModel(PersistentModel):
    foo: str = "foo"
    bar: int = 88
    enum: EnumForTest = EnumForTest.foo
    model: PydanticModel = PydanticModel()


class TestPersistedModel:
    @staticmethod
    def test_persisted_model_is_persisted_when_created():
        model = PersistedModel(
            foo="test",
            bar=99,
            enum=EnumForTest.bar,
            model=PydanticModel(foo="tes", bar=False),
        )

        pth = pathlib.Path("PersistedModel.json")
        assert (
            pth.exists()
        ), "Creation of model didn't create model persistence file on disk"
        loaded_model = PersistedModel.load()
        assert (
            model == loaded_model
        ), "loaded model from persistence file does not match original"
        assert loaded_model.enum == EnumForTest.bar
        assert loaded_model.model == PydanticModel(foo="tes", bar=False)

    @staticmethod
    def test_persisted_model_is_persisted_when_modified():
        model = PersistedModel()

        model.foo = "changed"

        loaded_model = PersistedModel.load()
        assert (
            model == loaded_model
        ), "loaded model from persistence file does not match original"

    @staticmethod
    def test_persisted_model_is_not_persisted_when_nested_model_is_modified():
        """This test is to show that modifying nested model doesn't trigger save - which may lead to errors.
        Watch out for it - in that case, use save() method"""
        model = PersistedModel()

        model.model.foo = "changed"

        loaded_model = PersistedModel.load()
        assert (
            model != loaded_model
        ), "loaded model from persistence file does not match original"
