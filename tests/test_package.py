import pyqt5libs


def test_package_exposes_version():
    assert isinstance(pyqt5libs.__version__, str)
    assert pyqt5libs.__version__
