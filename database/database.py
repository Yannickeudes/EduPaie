import os
import shutil
import sqlite3
import sys


def obtenir_dossier_projet():
    return os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )


def obtenir_chemin_base():
    if getattr(sys, "frozen", False):
        dossier_exe = os.path.dirname(
            sys.executable
        )

        return os.path.join(
            dossier_exe,
            "database",
            "edupaie.db"
        )

    return os.path.join(
        obtenir_dossier_projet(),
        "database",
        "edupaie.db"
    )


def obtenir_chemin_base_embarquee():
    dossier_temporaire = getattr(
        sys,
        "_MEIPASS",
        obtenir_dossier_projet()
    )

    return os.path.join(
        dossier_temporaire,
        "database",
        "edupaie.db"
    )


def obtenir_chemin_schema():
    return os.path.join(
        obtenir_dossier_projet(),
        "database",
        "schema.sql"
    )


def initialiser_base():
    chemin_base = obtenir_chemin_base()

    os.makedirs(
        os.path.dirname(chemin_base),
        exist_ok=True
    )

    if getattr(sys, "frozen", False):
        chemin_base_embarquee = (
            obtenir_chemin_base_embarquee()
        )

        if (
            not os.path.exists(chemin_base)
            and os.path.exists(chemin_base_embarquee)
        ):
            shutil.copy2(
                chemin_base_embarquee,
                chemin_base
            )

    base_existe = os.path.exists(
        chemin_base
    )

    connection = sqlite3.connect(
        chemin_base
    )

    if not base_existe:
        chemin_schema = obtenir_chemin_schema()

        if os.path.exists(chemin_schema):
            with open(
                chemin_schema,
                "r",
                encoding="utf-8"
            ) as file:
                schema = file.read()

            connection.executescript(schema)

    return connection