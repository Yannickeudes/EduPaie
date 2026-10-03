import sqlite3


class PaiementRepository:
    def __init__(self, connection):
        self.connection = connection

    def ajouter(
        self,
        numero_recu,
        eleve_id,
        montant,
        date_paiement,
        mode_paiement
    ):
        query = """
            INSERT INTO paiements
            (
                numero_recu,
                eleve_id,
                montant,
                date_paiement,
                mode_paiement
            )
            VALUES (?, ?, ?, ?, ?)
        """

        cursor = self.connection.execute(
            query,
            (
                numero_recu,
                eleve_id,
                montant,
                date_paiement,
                mode_paiement
            )
        )

        self.connection.commit()
        return cursor.lastrowid

    def lister(self):
        query = """
            SELECT
                id,
                numero_recu,
                eleve_id,
                montant,
                date_paiement,
                mode_paiement
            FROM paiements
            ORDER BY date_paiement DESC, id DESC
        """

        cursor = self.connection.execute(query)
        return cursor.fetchall()

    def lister_par_eleve(self, eleve_id):
        query = """
            SELECT
                id,
                numero_recu,
                eleve_id,
                montant,
                date_paiement,
                mode_paiement
            FROM paiements
            WHERE eleve_id = ?
            ORDER BY date_paiement ASC, id ASC
        """

        cursor = self.connection.execute(query, (eleve_id,))
        return cursor.fetchall()