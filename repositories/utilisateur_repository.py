class UtilisateurRepository:
    def __init__(self, connection):
        self.connection = connection

    def compter(self):
        curseur = self.connection.execute(
            "SELECT COUNT(*) FROM utilisateurs"
        )
        return curseur.fetchone()[0]

    def ajouter(
        self,
        role,
        nom,
        mot_de_passe_hash,
        sel
    ):
        self.connection.execute(
            """
            INSERT INTO utilisateurs
            (role, nom, mot_de_passe_hash, sel)
            VALUES (?, ?, ?, ?)
            """,
            (role, nom, mot_de_passe_hash, sel)
        )

        self.connection.commit()

    def trouver_par_role(self, role):
        curseur = self.connection.execute(
            """
            SELECT id, role, nom, mot_de_passe_hash, sel
            FROM utilisateurs
            WHERE role = ?
            """,
            (role,)
        )

        return curseur.fetchone()

    def mettre_a_jour_mot_de_passe(
        self,
        role,
        mot_de_passe_hash,
        sel
    ):
        self.connection.execute(
            """
            UPDATE utilisateurs
            SET mot_de_passe_hash = ?, sel = ?
            WHERE role = ?
            """,
            (mot_de_passe_hash, sel, role)
        )

        self.connection.commit()
