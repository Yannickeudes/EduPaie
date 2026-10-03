class EleveService:
    def __init__(
        self,
        eleve_repository,
        paiement_service
    ):
        self.eleve_repository = eleve_repository
        self.paiement_service = paiement_service

    def modifier_eleve(
        self,
        eleve_id,
        nom,
        prenom,
        classe,
        annee_scolaire,
        montant_total
    ):
        if not nom or not prenom or not classe or not annee_scolaire:
            raise ValueError(
                "Tous les champs sont obligatoires."
            )

        if montant_total <= 0:
            raise ValueError(
                "Le montant total doit être supérieur à 0."
            )

        eleve = self.eleve_repository.trouver_par_id(
            eleve_id
        )

        if eleve is None:
            raise ValueError(
                "Élève introuvable."
            )

        total_paye = (
            self.paiement_service.calculer_total_paye(
                eleve_id
            )
        )

        if montant_total < total_paye:
            raise ValueError(
                "Le nouveau montant total ne peut pas "
                "être inférieur au montant déjà payé."
            )

        self.eleve_repository.modifier(
            eleve_id,
            nom,
            prenom,
            classe,
            annee_scolaire,
            montant_total
        )

    def supprimer_eleve(self, eleve_id):
        eleve = self.eleve_repository.trouver_par_id(
            eleve_id
        )

        if eleve is None:
            raise ValueError(
                "Élève introuvable."
            )

        total_paye = (
            self.paiement_service.calculer_total_paye(
                eleve_id
            )
        )

        if total_paye > 0:
            raise ValueError(
                "Impossible de supprimer cet élève "
                "car des paiements sont déjà enregistrés."
            )

        self.eleve_repository.supprimer(
            eleve_id
        )