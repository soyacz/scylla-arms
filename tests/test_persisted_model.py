import pathlib
from enum import Enum

from pydantic import BaseModel

from scylla_arms.config import PersistentModel


class TestedEnum(Enum):
    foo: str = "foo"
    bar: str = "bar"


class PydanticModel(BaseModel):
    foo: str = "foo"
    bar: bool = True


class TestedPersistedModel(PersistentModel):
    foo: str = "foo"
    bar: int = 88
    enum: TestedEnum = TestedEnum.foo
    model: PydanticModel = PydanticModel()


class TestPersistedModel:
    def test_persisted_model_is_persisted_when_created(self):
        model = TestedPersistedModel(
            foo="test",
            bar=99,
            enum=TestedEnum.bar,
            model=PydanticModel(foo="tes", bar=False),
        )

        pth = pathlib.Path("TestedPersistedModel.json")
        assert (
            pth.exists()
        ), "Creation of model didn't create model persistence file on disk"
        loaded_model = TestedPersistedModel.load()
        assert (
            model == loaded_model
        ), "loaded model from persistence file does not match original"
        assert loaded_model.enum == TestedEnum.bar
        assert loaded_model.model == PydanticModel(foo="tes", bar=False)

    def test_persisted_model_is_persisted_when_modified(self):
        model = TestedPersistedModel()

        model.foo = "changed"

        loaded_model = TestedPersistedModel.load()
        assert (
            model == loaded_model
        ), "loaded model from persistence file does not match original"

    def test_persisted_model_is_not_persisted_when_nested_model_is_modified(self):
        """This test is to show that modifying nested model doesn't trigger save - which may lead to errors.
        Watch out for it - in that case, use save() method"""
        model = TestedPersistedModel()

        model.model.foo = "changed"

        loaded_model = TestedPersistedModel.load()
        assert (
            model != loaded_model
        ), "loaded model from persistence file does not match original"
