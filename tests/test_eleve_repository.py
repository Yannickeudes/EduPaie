import sqlite3
import unittest

from repositories.eleve_repository import EleveRepository


class TestEleveRepository(unittest.TestCase):

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

        self.repository = EleveRepository(
            self.connection
        )

    def tearDown(self):
        self.connection.close()

    def test_ajouter_eleve(self):
        eleve_id = self.repository.ajouter(
            "DIALLO",
            "Aminata",
            "Terminale A",
            "2026-2027",
            200000
        )

        eleve = self.repository.trouver_par_id(
            eleve_id
        )

        self.assertIsNotNone(eleve)
        self.assertEqual(eleve[1], "DIALLO")
        self.assertEqual(eleve[2], "Aminata")
        self.assertEqual(eleve[3], "Terminale A")
        self.assertEqual(eleve[4], "2026-2027")
        self.assertEqual(eleve[5], 200000)

    def test_rechercher_par_nom(self):
        self.repository.ajouter(
            "DIALLO",
            "Aminata",
            "Terminale A",
            "2026-2027",
            200000
        )

        self.repository.ajouter(
            "KOFFI",
            "Jean",
            "Première A",
            "2026-2027",
            180000
        )

        resultats = self.repository.rechercher(
            "DIALLO"
        )

        self.assertEqual(len(resultats), 1)
        self.assertEqual(
            resultats[0][1],
            "DIALLO"
        )

    def test_filtrer_par_classe(self):
        self.repository.ajouter(
            "DIALLO",
            "Aminata",
            "Terminale A",
            "2026-2027",
            200000
        )

        self.repository.ajouter(
            "KOFFI",
            "Jean",
            "Première A",
            "2026-2027",
            180000
        )

        resultats = self.repository.rechercher(
            classe="Terminale A"
        )

        self.assertEqual(len(resultats), 1)
        self.assertEqual(
            resultats[0][3],
            "Terminale A"
        )

    def test_modifier_eleve(self):
        eleve_id = self.repository.ajouter(
            "DIALLO",
            "Aminata",
            "Terminale A",
            "2026-2027",
            200000
        )

        self.repository.modifier(
            eleve_id,
            "KOFFI",
            "Jean",
            "Terminale B",
            "2026-2027",
            220000
        )

        eleve = self.repository.trouver_par_id(
            eleve_id
        )

        self.assertEqual(eleve[1], "KOFFI")
        self.assertEqual(eleve[2], "Jean")
        self.assertEqual(eleve[3], "Terminale B")
        self.assertEqual(eleve[5], 220000)

    def test_supprimer_eleve(self):
        eleve_id = self.repository.ajouter(
            "DIALLO",
            "Aminata",
            "Terminale A",
            "2026-2027",
            200000
        )

        self.repository.supprimer(eleve_id)

        eleve = self.repository.trouver_par_id(
            eleve_id
        )

        self.assertIsNone(eleve)


if __name__ == "__main__":
    unittest.main()