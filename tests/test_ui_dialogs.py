from pyqt5libs.ui import dialogs


def test_dialogs_module_exposes_public_helpers():
    assert dialogs.DEFAULT_TITLE == "Sistema"
    assert callable(dialogs.show_info)
    assert callable(dialogs.show_warning)
    assert callable(dialogs.show_error)
    assert callable(dialogs.ask_yes_no)
    assert callable(dialogs.confirm)


def test_dialogs_module_all_is_defined():
    assert "show_info" in dialogs.__all__
    assert "show_warning" in dialogs.__all__
    assert "show_error" in dialogs.__all__
    assert "ask_yes_no" in dialogs.__all__
    assert "confirm" in dialogs.__all__
