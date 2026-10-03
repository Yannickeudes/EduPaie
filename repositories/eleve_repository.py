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

    def modifier(self, eleve_id, nom, prenom, classe, annee_scolaire, montant_total):
        query = """
            UPDATE eleves
            SET nom = ?,
                prenom = ?,
                classe = ?,
                annee_scolaire = ?,
                montant_total = ?
            WHERE id = ?
        """

        self.connection.execute(
            query,
            (nom, prenom, classe, annee_scolaire, montant_total, eleve_id)
        )

        self.connection.commit()

    def supprimer(self, eleve_id):
        query = "DELETE FROM eleves WHERE id = ?"

        self.connection.execute(query, (eleve_id,))
        self.connection.commit()