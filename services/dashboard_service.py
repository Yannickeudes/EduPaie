
class DashboardService:
    def __init__(self, eleve_repository, paiement_service):
        self.eleve_repository = eleve_repository
        self.paiement_service = paiement_service

    def nombre_eleves(self):
        return len(self.eleve_repository.lister())

    def total_encaisse(self):
        eleves = self.eleve_repository.lister()

        total = 0

        for eleve in eleves:
            total += self.paiement_service.calculer_total_paye(
                eleve[0]
            )

        return total

    def total_restant(self):
        eleves = self.eleve_repository.lister()

        total = 0

        for eleve in eleves:
            total += self.paiement_service.calculer_solde(
                eleve[0]
            )

        return total

    def nombre_non_soldes(self):
        eleves = self.eleve_repository.lister()

        nombre = 0

        for eleve in eleves:
            statut = self.paiement_service.determiner_statut(
                eleve[0]
            )

            if statut != "Soldé":
                nombre += 1

        return nombre

    def lister_eleves_avec_statut(self):
        eleves = self.eleve_repository.lister()

        resultat = []

        for eleve in eleves:
            resultat.append(
                {
                    "id": eleve[0],
                    "nom": eleve[1],
                    "prenom": eleve[2],
                    "classe": eleve[3],
                    "annee_scolaire": eleve[4],
                    "montant_total": eleve[5],
                    "total_paye": self.paiement_service.calculer_total_paye(
                        eleve[0]
                    ),
                    "solde": self.paiement_service.calculer_solde(
                        eleve[0]
                    ),
                    "statut": self.paiement_service.determiner_statut(
                        eleve[0]
                    )
                }
            )

        return resultat
