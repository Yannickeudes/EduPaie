class ParametreRepository:
    def __init__(self, connection):
        self.connection = connection

    def obtenir(self, cle, defaut=None):
        curseur = self.connection.execute(
            "SELECT valeur FROM parametres WHERE cle = ?",
            (cle,)
        )

        ligne = curseur.fetchone()

        if ligne is None:
            return defaut

        return ligne[0]

    def definir(self, cle, valeur):
        self.connection.execute(
            """
            INSERT INTO parametres (cle, valeur)
            VALUES (?, ?)
            ON CONFLICT(cle) DO UPDATE SET valeur = excluded.valeur
            """,
            (cle, valeur)
        )

        self.connection.commit()

    def tout(self):
        curseur = self.connection.execute(
            "SELECT cle, valeur FROM parametres"
        )

        return {
            ligne[0]: ligne[1]
            for ligne in curseur.fetchall()
        }
