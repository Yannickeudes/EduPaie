class PaiementRepository:
    def __init__(self, connection):
        self.connection = connection

    def ajouter(
        self,
        numero_recu,
        eleve_id,
        montant,
        date_paiement,
        mode_paiement,
        solde_apres_paiement
    ):
        query = """
            INSERT INTO paiements
            (
                numero_recu,
                eleve_id,
                montant,
                date_paiement,
                mode_paiement,
                solde_apres_paiement
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """

        cursor = self.connection.execute(
            query,
            (
                numero_recu,
                eleve_id,
                montant,
                date_paiement,
                mode_paiement,
                solde_apres_paiement
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
                mode_paiement,
                solde_apres_paiement
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
                mode_paiement,
                solde_apres_paiement
            FROM paiements
            WHERE eleve_id = ?
            ORDER BY date_paiement ASC, id ASC
        """

        cursor = self.connection.execute(
            query,
            (eleve_id,)
        )

        return cursor.fetchall()

    def prochain_numero(self, annee):
        curseur = self.connection.execute(
            """
            SELECT numero_recu
            FROM paiements
            WHERE numero_recu LIKE ?
            """,
            (f"REC-{annee}-%",)
        )

        numeros = [
            ligne[0] for ligne in curseur.fetchall()
        ]

        maximum = 0

        for numero in numeros:
            try:
                suffixe = int(numero.rsplit("-", 1)[1])
            except (ValueError, IndexError):
                continue

            maximum = max(maximum, suffixe)

        return f"REC-{annee}-{maximum + 1:04d}"

    def trouver_par_numero_recu(self, numero_recu):
        query = """
            SELECT
                id,
                numero_recu,
                eleve_id,
                montant,
                date_paiement,
                mode_paiement,
                solde_apres_paiement
            FROM paiements
            WHERE numero_recu = ?
        """

        cursor = self.connection.execute(
            query,
            (numero_recu,)
        )

        return cursor.fetchone()

    def trouver_par_id(self, paiement_id):
        query = """
            SELECT
                id,
                numero_recu,
                eleve_id,
                montant,
                date_paiement,
                mode_paiement,
                solde_apres_paiement
            FROM paiements
            WHERE id = ?
        """

        cursor = self.connection.execute(
            query,
            (paiement_id,)
        )

        return cursor.fetchone()