"""Ejemplo funcional de AutoABM con Peewee, SQLite y PyQt5.

Ejecutar desde la raíz del repo:

    python examples/autoabm_clientes/main.py
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from peewee import BooleanField, CharField, Model, SqliteDatabase
from PyQt5.QtWidgets import QApplication

from pyqt5libs.generators.abm import create_abm_from_model
from pyqt5libs.styles.fluent import fluent_abm_stylesheet

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "clientes.db"
db = SqliteDatabase(DB_PATH)


class BaseModel(Model):
    class Meta:
        database = db


class Cliente(BaseModel):
    nombre = CharField(max_length=100)
    email = CharField(max_length=120, null=True)
    telefono = CharField(max_length=50, null=True)
    activo = BooleanField(default=True)

    def __str__(self):
        return self.nombre


def initialize_database():
    db.connect(reuse_if_open=True)
    db.create_tables([Cliente])

    if Cliente.select().count() == 0:
        Cliente.create(nombre="Oscar Vogel", email="oscar@example.com", telefono="3755-000000")
        Cliente.create(nombre="Cliente Demo", email="demo@example.com", telefono="3755-111111")


def build_window_class():
    return create_abm_from_model(
        Cliente,
        title="Clientes",
        form_columns=2,
        view_mode="split",
        visible_primary_key=False,
        include_read_only_fields=False,
    )


def run_manual_persistence_check(ClientesABM):
    """Prueba rápida de métodos productivos sin depender de interacción visual."""
    instance = ClientesABM()

    validation = instance.ValidateValues({"nombre": "", "email": "mal"})
    assert not validation.ok

    create_result = instance.CreateRecord(
        {
            "nombre": "Cliente creado desde AutoABM",
            "email": "autoabm@example.com",
            "telefono": "3755-222222",
            "activo": True,
        }
    )
    assert create_result.ok

    update_result = instance.UpdateRecord(
        create_result.record,
        {
            "nombre": "Cliente actualizado desde AutoABM",
            "email": "actualizado@example.com",
            "telefono": "3755-333333",
            "activo": True,
        },
    )
    assert update_result.ok

    remove_result = instance.RemoveRecord(update_result.record)
    assert remove_result.ok


def main():
    initialize_database()
    ClientesABM = build_window_class()
    app = QApplication(sys.argv)
    app.setStyleSheet(fluent_abm_stylesheet())

    # Verificación mínima de producción antes de abrir la ventana.
    run_manual_persistence_check(ClientesABM)

    window = ClientesABM()
    window.setMinimumSize(1180, 720)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
