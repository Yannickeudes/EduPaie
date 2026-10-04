import sqlite3
import unittest

from repositories.eleve_repository import EleveRepository
from repositories.paiement_repository import PaiementRepository


class TestPaiementRepository(unittest.TestCase):

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
                mode_paiement TEXT NOT NULL,
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

    def tearDown(self):
        self.connection.close()

    def creer_eleve(self):
        return self.eleve_repository.ajouter(
            "TEST",
            "Historique",
            "Terminale A",
            "2026-2027",
            200000
        )

    def ajouter_paiements(self, eleve_id):
        self.paiement_repository.ajouter(
            "REC-HIST-001",
            eleve_id,
            50000,
            "2026-10-03",
            "Mobile Money",
            150000
        )

        self.paiement_repository.ajouter(
            "REC-HIST-002",
            eleve_id,
            30000,
            "2026-10-05",
            "Espèces",
            120000
        )

        self.paiement_repository.ajouter(
            "REC-HIST-003",
            eleve_id,
            40000,
            "2026-10-10",
            "Virement",
            80000
        )

    def test_ajouter_paiement(self):
        eleve_id = self.creer_eleve()

        paiement_id = (
            self.paiement_repository.ajouter(
                "REC-HIST-001",
                eleve_id,
                50000,
                "2026-10-03",
                "Mobile Money",
                150000
            )
        )

        paiement = (
            self.paiement_repository
            .trouver_par_id(paiement_id)
        )

        self.assertIsNotNone(paiement)
        self.assertEqual(
            paiement[1],
            "REC-HIST-001"
        )
        self.assertEqual(
            paiement[2],
            eleve_id
        )
        self.assertEqual(
            paiement[3],
            50000
        )
        self.assertEqual(
            paiement[6],
            150000
        )

    def test_lister_par_eleve(self):
        eleve_id = self.creer_eleve()

        self.ajouter_paiements(eleve_id)

        historique = (
            self.paiement_repository
            .lister_par_eleve(eleve_id)
        )

        self.assertEqual(
            len(historique),
            3
        )

        self.assertEqual(
            historique[0][1],
            "REC-HIST-001"
        )

        self.assertEqual(
            historique[1][1],
            "REC-HIST-002"
        )

        self.assertEqual(
            historique[2][1],
            "REC-HIST-003"
        )

    def test_trouver_par_numero_recu(self):
        eleve_id = self.creer_eleve()

        self.ajouter_paiements(eleve_id)

        paiement = (
            self.paiement_repository
            .trouver_par_numero_recu(
                "REC-HIST-002"
            )
        )

        self.assertIsNotNone(paiement)

        self.assertEqual(
            paiement[1],
            "REC-HIST-002"
        )

        self.assertEqual(
            paiement[3],
            30000
        )

        self.assertEqual(
            paiement[6],
            120000
        )

    def test_trouver_paiement_inexistant(self):
        paiement = (
            self.paiement_repository
            .trouver_par_numero_recu(
                "REC-INEXISTANT"
            )
        )

        self.assertIsNone(paiement)

    def test_lister_paiements(self):
        eleve_id = self.creer_eleve()

        self.ajouter_paiements(eleve_id)

        paiements = (
            self.paiement_repository.lister()
        )

        self.assertEqual(
            len(paiements),
            3
        )


if __name__ == "__main__":
    unittest.main()