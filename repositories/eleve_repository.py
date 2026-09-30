import sqlite3


class EleveRepository:
    def __init__(self, connection):
        self.connection = connection

    def ajouter(self, nom, prenom, classe, annee_scolaire, montant_total):
        query = """
            INSERT INTO eleves
            (nom, prenom, classe, annee_scolaire, montant_total)
            VALUES (?, ?, ?, ?, ?)
        """

        cursor = self.connection.execute(
            query,
            (nom, prenom, classe, annee_scolaire, montant_total)
        )

        self.connection.commit()
        return cursor.lastrowid

    def lister(self):
        query = """
            SELECT id, nom, prenom, classe, annee_scolaire, montant_total
            FROM eleves
            ORDER BY nom, prenom
        """

        cursor = self.connection.execute(query)
        return cursor.fetchall()