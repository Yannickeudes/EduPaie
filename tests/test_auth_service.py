import sqlite3
import unittest

from repositories.utilisateur_repository import UtilisateurRepository
from services.auth_service import AuthService, ROLES


class TestAuthService(unittest.TestCase):

    def setUp(self):
        self.connection = sqlite3.connect(":memory:")

        self.connection.executescript("""
            CREATE TABLE utilisateurs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL UNIQUE,
                nom TEXT NOT NULL,
                mot_de_passe_hash TEXT NOT NULL,
                sel TEXT NOT NULL
            );
        """)

        self.repository = UtilisateurRepository(
            self.connection
        )

        self.service = AuthService(self.repository)

    def test_comptes_non_configures(self):
        self.assertFalse(
            self.service.comptes_configures()
        )

    def test_configurer_et_verifier(self):
        self.service.configurer_comptes({
            "Directeur": "direct123",
            "Comptable": "compta123",
            "Secrétaire": "secret123",
        })

        self.assertTrue(
            self.service.comptes_configures()
        )

        mots_de_passe = {
            "Directeur": "direct123",
            "Comptable": "compta123",
            "Secrétaire": "secret123",
        }

        for role in ROLES:
            self.assertTrue(
                self.service.verifier(
                    role,
                    mots_de_passe[role]
                )
            )

    def test_mauvais_mot_de_passe(self):
        self.service.configurer_comptes({
            "Directeur": "direct123",
            "Comptable": "compta123",
            "Secrétaire": "secret123",
        })

        self.assertFalse(
            self.service.verifier("Directeur", "mauvais")
        )

    def test_mot_de_passe_trop_court(self):
        with self.assertRaises(ValueError):
            self.service.configurer_comptes({
                "Directeur": "abc",
                "Comptable": "compta123",
                "Secrétaire": "secret123",
            })

    def test_changer_mot_de_passe(self):
        self.service.configurer_comptes({
            "Directeur": "direct123",
            "Comptable": "compta123",
            "Secrétaire": "secret123",
        })

        self.service.changer_mot_de_passe(
            "Directeur",
            "direct123",
            "nouveau456"
        )

        self.assertFalse(
            self.service.verifier("Directeur", "direct123")
        )

        self.assertTrue(
            self.service.verifier("Directeur", "nouveau456")
        )

    def test_changer_mot_de_passe_incorrect(self):
        self.service.configurer_comptes({
            "Directeur": "direct123",
            "Comptable": "compta123",
            "Secrétaire": "secret123",
        })

        with self.assertRaises(ValueError):
            self.service.changer_mot_de_passe(
                "Directeur",
                "mauvais",
                "nouveau456"
            )


if __name__ == "__main__":
    unittest.main()
