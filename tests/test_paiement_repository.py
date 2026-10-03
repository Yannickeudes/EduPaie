import sqlite3

from repositories.eleve_repository import EleveRepository
from repositories.paiement_repository import PaiementRepository


connection = sqlite3.connect("database/edupaie.db")

eleve_repository = EleveRepository(connection)
paiement_repository = PaiementRepository(connection)

# Élève de test
eleve_id = eleve_repository.ajouter(
    "TEST",
    "Historique",
    "Terminale A",
    "2026-2027",
    200000
)

# Plusieurs paiements avec des dates différentes
paiement_repository.ajouter(
    "REC-HIST-001",
    eleve_id,
    50000,
    "2026-10-03",
    "Mobile Money"
)

paiement_repository.ajouter(
    "REC-HIST-002",
    eleve_id,
    30000,
    "2026-10-05",
    "Espèces"
)

paiement_repository.ajouter(
    "REC-HIST-003",
    eleve_id,
    40000,
    "2026-10-10",
    "Virement"
)

# Historique de l'élève
historique = paiement_repository.lister_par_eleve(eleve_id)

print("Historique des paiements :")

for paiement in historique:
    print(paiement)

# Recherche d'un paiement précis
paiement = paiement_repository.trouver_par_numero_recu(
    "REC-HIST-002"
)

print("Paiement retrouvé :", paiement)

# Nettoyage
connection.execute(
    "DELETE FROM paiements WHERE eleve_id = ?",
    (eleve_id,)
)

connection.commit()

eleve_repository.supprimer(eleve_id)

connection.close()