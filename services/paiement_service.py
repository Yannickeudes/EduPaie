class PaiementService:
    def __init__(self, eleve_repository, paiement_repository):
        self.eleve_repository = eleve_repository
        self.paiement_repository = paiement_repository

    def calculer_total_paye(self, eleve_id):
        paiements = self.paiement_repository.lister_par_eleve(eleve_id)

        total_paye = sum(paiement[3] for paiement in paiements)

        return total_paye

    def calculer_solde(self, eleve_id):
        eleves = self.eleve_repository.lister()

        for eleve in eleves:
            if eleve[0] == eleve_id:
                montant_total = eleve[5]
                total_paye = self.calculer_total_paye(eleve_id)

                return montant_total - total_paye

        raise ValueError("Élève introuvable.")

    def enregistrer_paiement(
        self,
        numero_recu,
        eleve_id,
        montant,
        date_paiement,
        mode_paiement
    ):
        if montant <= 0:
            raise ValueError("Le montant du paiement doit être supérieur à 0.")

        solde = self.calculer_solde(eleve_id)

        if montant > solde:
            raise ValueError(
                "Le montant du paiement dépasse le solde restant."
            )

        return self.paiement_repository.ajouter(
            numero_recu,
            eleve_id,
            montant,
            date_paiement,
            mode_paiement
        )

    def determiner_statut(self, eleve_id):
        solde = self.calculer_solde(eleve_id)

        if solde == 0:
            return "Soldé"

        total_paye = self.calculer_total_paye(eleve_id)

        if total_paye == 0:
            return "Non payé"

        return "Partiellement payé"