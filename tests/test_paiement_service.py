import sqlite3
import unittest

from repositories.eleve_repository import EleveRepository
from repositories.paiement_repository import PaiementRepository
from services.paiement_service import PaiementService


class TestPaiementService(unittest.TestCase):

    def setUp(self):
        self.connection = sqlite3.connect(":memory:")

        self.connection.execute(
            "PRAGMA foreign_keys = ON"
        )

        self.connection.executescript("""
            CREATE TABLE eleves (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                prenom TEXT NOT NULL,
                classe TEXT NOT NULL,
                annee_scolaire TEXT NOT NULL,
                montant_total REAL NOT NULL
                    CHECK(montant_total >= 0)
            );

            CREATE TABLE paiements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_recu TEXT NOT NULL UNIQUE,
                eleve_id INTEGER NOT NULL,
                montant REAL NOT NULL
                    CHECK(montant > 0),
                date_paiement TEXT NOT NULL,
                mode_paiement TEXT NOT NULL
                    CHECK (
                        mode_paiement IN (
                            'Espèces',
                            'Chèque',
                            'Virement',
                            'Mobile Money'
                        )
                    ),
                solde_apres_paiement REAL NOT NULL
                    CHECK(solde_apres_paiement >= 0),
                FOREIGN KEY (eleve_id)
                    REFERENCES eleves(id)
            );
        """)

        self.eleve_repository = EleveRepository(
            self.connection
        )

        self.paiement_repository = PaiementRepository(
            self.connection
        )

        self.service = PaiementService(
            self.eleve_repository,
            self.paiement_repository
        )

    def tearDown(self):
        self.connection.close()

    def test_paiement_normal(self):
        eleve_id = self.eleve_repository.ajouter(
            "TEST",
            "Service",
            "Terminale A",
            "2026-2027",
            200000
        )

        self.service.enregistrer_paiement(
            "REC-SERVICE-001",
            eleve_id,
            50000,
            "2026-10-03",
            "Mobile Money"
        )

        self.assertEqual(
            self.service.calculer_total_paye(eleve_id),
            50000
        )

        self.assertEqual(
            self.service.calculer_solde(eleve_id),
            150000
        )

    def test_paiement_superieur_au_solde(self):
        eleve_id = self.eleve_repository.ajouter(
            "TEST",
            "Service",
            "Terminale A",
            "2026-2027",
            200000
        )

        self.service.enregistrer_paiement(
            "REC-SERVICE-001",
            eleve_id,
            50000,
            "2026-10-03",
            "Mobile Money"
        )

        with self.assertRaises(ValueError):
            self.service.enregistrer_paiement(
                "REC-SERVICE-002",
                eleve_id,
                200000,
                "2026-10-03",
                "Espèces"
            )

    def test_statut_partiellement_paye(self):
        eleve_id = self.eleve_repository.ajouter(
            "TEST",
            "Partiel",
            "Terminale A",
            "2026-2027",
            200000
        )

        self.service.enregistrer_paiement(
            "REC-SERVICE-001",
            eleve_id,
            50000,
            "2026-10-03",
            "Mobile Money"
        )

        self.assertEqual(
            self.service.determiner_statut(eleve_id),
            "Partiellement payé"
        )

    def test_statut_non_paye(self):
        eleve_id = self.eleve_repository.ajouter(
            "TEST",
            "NonPaye",
            "Seconde",
            "2026-2027",
            100000
        )

        self.assertEqual(
            self.service.determiner_statut(eleve_id),
            "Non payé"
        )

    def test_statut_solde(self):
        eleve_id = self.eleve_repository.ajouter(
            "TEST",
            "Solde",
            "Première",
            "2026-2027",
            100000
        )

        self.service.enregistrer_paiement(
            "REC-SERVICE-001",
            eleve_id,
            100000,
            "2026-10-03",
            "Virement"
        )

        self.assertEqual(
            self.service.determiner_statut(eleve_id),
            "Soldé"
        )


if __name__ == "__main__":
    unittest.main()