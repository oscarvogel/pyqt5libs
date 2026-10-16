import importlib
import sys
import types
from pathlib import Path


repository_root = Path(__file__).resolve().parents[1]
vendored_package = types.ModuleType("vendored_pyqt5libs")
vendored_package.__path__ = [str(repository_root)]
sys.modules.setdefault("vendored_pyqt5libs", vendored_package)
utiles = importlib.import_module("vendored_pyqt5libs.pyqt5libs.utiles")
constantes = importlib.import_module("vendored_pyqt5libs.pyqt5libs.Constantes")


def test_sitio_web_vogel_default_usa_branding_actual(monkeypatch):
    monkeypatch.delenv("FGPY_SITIO_WEB", raising=False)
    monkeypatch.setattr(utiles, "LeerIni", lambda *args, **kwargs: "")

    assert utiles.sitio_web_vogel() == "https://vogelconsultoria.com.ar"
    assert "servinlgsm" not in utiles.sitio_web_vogel().lower()


def test_sitio_web_vogel_respeta_variable_de_entorno(monkeypatch):
    monkeypatch.setenv("FGPY_SITIO_WEB", "https://ejemplo.test")
    monkeypatch.setattr(utiles, "LeerIni", lambda *args, **kwargs: "")

    assert utiles.sitio_web_vogel() == "https://ejemplo.test"


def test_sitio_web_vogel_respeta_ini(monkeypatch):
    monkeypatch.delenv("FGPY_SITIO_WEB", raising=False)
    monkeypatch.setattr(
        utiles,
        "LeerIni",
        lambda clave=None, **kwargs: "https://ini.test" if clave == "sitio_web" else "",
    )

    assert utiles.sitio_web_vogel() == "https://ini.test"


def test_empresa_actual_y_legacy_definidas():
    assert constantes.EMPRESA == "Vogel Consultoria"
    assert constantes.EMPRESA_LEGACY == "Servin LGSM"
    assert constantes.SITIO_WEB == "https://vogelconsultoria.com.ar"
