import json

import pytest

from scylla_arms.persisted_dicts import FilePersistedDotDict


class TestFilePersistedDotDict:
    @staticmethod
    def test_attribute_can_be_set_and_is_saved_to_file(tmp_path):
        persist_file_path = tmp_path / "pfile"
        file_persisted_dot_dict_data = FilePersistedDotDict(persist_file_path)
        file_persisted_dot_dict_data.att = "test"

        assert file_persisted_dot_dict_data.att == "test"

        with open(persist_file_path, "r", encoding="utf-8") as p_file:
            data = json.load(p_file)
            assert data["att"] == "test"

    @staticmethod
    def test_attribute_can_be_set_as_attribute_and_is_saved_to_file(tmp_path):
        persist_file_path = tmp_path / "pfile"
        file_persisted_dot_dict_data = FilePersistedDotDict(persist_file_path)
        file_persisted_dot_dict_data["att"] = "test"

        assert file_persisted_dot_dict_data.att == "test"

        with open(persist_file_path, "r", encoding="utf-8") as p_file:
            data = json.load(p_file)
            assert data["att"] == "test"

    @staticmethod
    def test_attribute_can_be_deleted_and_is_saved_to_file(tmp_path):
        persist_file_path = tmp_path / "pfile"
        file_persisted_dot_dict_data = FilePersistedDotDict(persist_file_path)
        file_persisted_dot_dict_data.att = "test"

        del file_persisted_dot_dict_data.att

        with pytest.raises(AttributeError):
            _ = file_persisted_dot_dict_data.att
        with open(persist_file_path, "r", encoding="utf-8") as p_file:
            data = json.load(p_file)
            assert "att" not in data.keys()

    @staticmethod
    def test_all_attributes_can_be_cleared(tmp_path):
        persist_file_path = tmp_path / "pfile"
        file_persisted_dot_dict_data = FilePersistedDotDict(persist_file_path)
        file_persisted_dot_dict_data.att_a = "test"
        file_persisted_dot_dict_data.att_b = "test"

        file_persisted_dot_dict_data.clear()

        assert "att_a" not in file_persisted_dot_dict_data
        assert "att_b" not in file_persisted_dot_dict_data

        with open(persist_file_path, "r", encoding="utf-8") as p_file:
            json_data = json.load(p_file)
            assert "att_a" not in json_data.keys()
            assert "att_b" not in json_data.keys()

    @staticmethod
    def test_can_update_multiple_attributes(tmp_path):
        persist_file_path = tmp_path / "pfile"
        file_persisted_dot_dict_data = FilePersistedDotDict(persist_file_path)
        file_persisted_dot_dict_data.att_a = "test"
        file_persisted_dot_dict_data.att_b = "test"

        file_persisted_dot_dict_data.update(att_a="new", att_c="test")

        assert file_persisted_dot_dict_data.att_a == "new"
        assert file_persisted_dot_dict_data.att_b == "test"
        assert file_persisted_dot_dict_data.att_c == "test"
