import sqlite3
import unittest

from repositories.eleve_repository import EleveRepository
from repositories.paiement_repository import PaiementRepository
from services.paiement_service import PaiementService
from services.dashboard_service import DashboardService


class TestDashboardService(unittest.TestCase):

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

        self.paiement_service = PaiementService(
            self.eleve_repository,
            self.paiement_repository
        )

        self.dashboard_service = DashboardService(
            self.eleve_repository,
            self.paiement_service
        )

    def tearDown(self):
        self.connection.close()

    def creer_donnees(self):
        eleve_1 = self.eleve_repository.ajouter(
            "TEST",
            "Dashboard1",
            "Terminale A",
            "2026-2027",
            200000
        )

        eleve_2 = self.eleve_repository.ajouter(
            "TEST",
            "Dashboard2",
            "Terminale B",
            "2026-2027",
            150000
        )

        self.paiement_service.enregistrer_paiement(
            "REC-DASH-001",
            eleve_1,
            100000,
            "2026-10-03",
            "Mobile Money"
        )

        self.paiement_service.enregistrer_paiement(
            "REC-DASH-002",
            eleve_2,
            150000,
            "2026-10-04",
            "Espèces"
        )

        return eleve_1, eleve_2

    def test_nombre_eleves(self):
        self.creer_donnees()

        self.assertEqual(
            self.dashboard_service.nombre_eleves(),
            2
        )

    def test_total_encaisse(self):
        self.creer_donnees()

        self.assertEqual(
            self.dashboard_service.total_encaisse(),
            250000
        )

    def test_total_restant(self):
        self.creer_donnees()

        self.assertEqual(
            self.dashboard_service.total_restant(),
            100000
        )

    def test_nombre_non_soldes(self):
        self.creer_donnees()

        self.assertEqual(
            self.dashboard_service.nombre_non_soldes(),
            1
        )

    def test_lister_eleves_avec_statut(self):
        eleve_1, eleve_2 = self.creer_donnees()

        resultats = (
            self.dashboard_service
            .lister_eleves_avec_statut()
        )

        self.assertEqual(len(resultats), 2)

        resultat_1 = next(
            eleve
            for eleve in resultats
            if eleve["id"] == eleve_1
        )

        resultat_2 = next(
            eleve
            for eleve in resultats
            if eleve["id"] == eleve_2
        )

        self.assertEqual(
            resultat_1["total_paye"],
            100000
        )

        self.assertEqual(
            resultat_1["solde"],
            100000
        )

        self.assertEqual(
            resultat_1["statut"],
            "Partiellement payé"
        )

        self.assertEqual(
            resultat_2["total_paye"],
            150000
        )

        self.assertEqual(
            resultat_2["solde"],
            0
        )

        self.assertEqual(
            resultat_2["statut"],
            "Soldé"
        )


if __name__ == "__main__":
    unittest.main()