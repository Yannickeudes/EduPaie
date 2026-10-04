import os
import unittest

from services.recu_service import RecuService


class TestRecuService(unittest.TestCase):

    def setUp(self):
        self.service = RecuService()

        self.eleve = (
            1,
            "DIALLO",
            "Aminata",
            "Terminale A",
            "2026-2027",
            200000
        )

        self.numero_recu = "REC-TEST-PDF-001"

        self.chemin = (
            f"receipts/{self.numero_recu}.pdf"
        )

    def tearDown(self):
        if os.path.exists(self.chemin):
            os.remove(self.chemin)

    def test_generer_recu(self):
        chemin = self.service.generer_recu(
            self.numero_recu,
            self.eleve,
            50000,
            "2026-10-03",
            "Mobile Money",
            150000
        )

        self.assertTrue(
            os.path.exists(chemin)
        )

        self.assertGreater(
            os.path.getsize(chemin),
            0
        )

        self.assertEqual(
            chemin,
            self.chemin
        )


if __name__ == "__main__":
    unittest.main()