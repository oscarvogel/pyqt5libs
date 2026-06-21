from pyqt5libs.core.config import IniConfig, load_ini, save_ini


def test_ini_config_can_set_save_and_read_values(tmp_path):
    path = tmp_path / "app.ini"

    IniConfig(path).set("database", "host", "localhost").set("database", "port", 3306).save()

    config = load_ini(path)

    assert config.exists()
    assert config.get("database", "host") == "localhost"
    assert config.get_int("database", "port") == 3306


def test_ini_config_returns_defaults_for_missing_values(tmp_path):
    path = tmp_path / "missing.ini"
    config = load_ini(path)

    assert config.get("app", "name", default="demo") == "demo"
    assert config.get_int("app", "port", default=8000) == 8000
    assert config.get_float("app", "ratio", default=1.5) == 1.5
    assert config.get_bool("app", "debug", default=False) is False


def test_ini_config_typed_getters(tmp_path):
    path = tmp_path / "typed.ini"

    save_ini(
        path,
        {
            "app": {
                "port": 8080,
                "ratio": "10,5",
                "debug": "si",
                "invalid_number": "abc",
            }
        },
    )

    config = load_ini(path)

    assert config.get_int("app", "port") == 8080
    assert config.get_float("app", "ratio") == 10.5
    assert config.get_bool("app", "debug") is True
    assert config.get_int("app", "invalid_number", default=1) == 1


def test_ini_config_as_dict(tmp_path):
    path = tmp_path / "dict.ini"

    save_ini(path, {"app": {"name": "Demo"}})
    config = load_ini(path)

    assert config.as_dict() == {"app": {"name": "Demo"}}


def test_ini_config_all_is_defined():
    from pyqt5libs.core import config

    assert "IniConfig" in config.__all__
    assert "load_ini" in config.__all__
    assert "save_ini" in config.__all__
