import sqlite3

from repositories.eleve_repository import EleveRepository
from repositories.paiement_repository import PaiementRepository
from services.paiement_service import PaiementService


connection = sqlite3.connect("database/edupaie.db")

eleve_repository = EleveRepository(connection)
paiement_repository = PaiementRepository(connection)

service = PaiementService(
    eleve_repository,
    paiement_repository
)

# Élève de test
eleve_id = eleve_repository.ajouter(
    "TEST",
    "Service",
    "Terminale A",
    "2026-2027",
    200000
)

# Paiement normal
service.enregistrer_paiement(
    "REC-SERVICE-001",
    eleve_id,
    50000,
    "2026-10-03",
    "Mobile Money"
)

print("Total payé :", service.calculer_total_paye(eleve_id))
print("Solde restant :", service.calculer_solde(eleve_id))

# Test d'un paiement supérieur au solde
try:
    service.enregistrer_paiement(
        "REC-SERVICE-002",
        eleve_id,
        200000,
        "2026-10-03",
        "Espèces"
    )
except ValueError as erreur:
    print("Paiement refusé :", erreur)

# Test du statut
print("Statut après paiement :", service.determiner_statut(eleve_id))
# Test du statut "Non payé"
eleve_non_paye = eleve_repository.ajouter(
    "TEST",
    "NonPaye",
    "Seconde",
    "2026-2027",
    100000
)

print(
    "Statut élève non payé :",
    service.determiner_statut(eleve_non_paye)
)

# Test du statut "Soldé"
eleve_solde = eleve_repository.ajouter(
    "TEST",
    "Solde",
    "Première",
    "2026-2027",
    100000
)

service.enregistrer_paiement(
    "REC-SERVICE-003",
    eleve_solde,
    100000,
    "2026-10-03",
    "Virement"
)

print(
    "Statut élève soldé :",
    service.determiner_statut(eleve_solde)
)

# Nettoyage
connection.execute(
    "DELETE FROM paiements WHERE eleve_id = ?",
    (eleve_id,)
)

connection.commit()

eleve_repository.supprimer(eleve_id)

connection.close()