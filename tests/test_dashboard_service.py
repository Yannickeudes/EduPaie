
import sqlite3

from repositories.eleve_repository import EleveRepository
from repositories.paiement_repository import PaiementRepository
from services.paiement_service import PaiementService
from services.dashboard_service import DashboardService


connection = sqlite3.connect("database/edupaie.db")

eleve_repository = EleveRepository(connection)
paiement_repository = PaiementRepository(connection)

paiement_service = PaiementService(
    eleve_repository,
    paiement_repository
)

dashboard_service = DashboardService(
    eleve_repository,
    paiement_service
)


# Création de deux élèves de test
eleve_1 = eleve_repository.ajouter(
    "TEST",
    "Dashboard1",
    "Terminale A",
    "2026-2027",
    200000
)

eleve_2 = eleve_repository.ajouter(
    "TEST",
    "Dashboard2",
    "Terminale B",
    "2026-2027",
    150000
)


# Paiements
paiement_service.enregistrer_paiement(
    "REC-DASH-001",
    eleve_1,
    100000,
    "2026-10-03",
    "Mobile Money"
)

paiement_service.enregistrer_paiement(
    "REC-DASH-002",
    eleve_2,
    150000,
    "2026-10-04",
    "Espèces"
)


# Tests du dashboard
print("Nombre d'élèves :", dashboard_service.nombre_eleves())
print("Total encaissé :", dashboard_service.total_encaisse())
print("Total restant :", dashboard_service.total_restant())
print("Nombre non soldés :", dashboard_service.nombre_non_soldes())

print("\nÉlèves avec statut :")

for eleve in dashboard_service.lister_eleves_avec_statut():
    print(eleve)


# Nettoyage
connection.execute(
    "DELETE FROM paiements WHERE numero_recu IN (?, ?)",
    ("REC-DASH-001", "REC-DASH-002")
)

connection.commit()

eleve_repository.supprimer(eleve_1)
eleve_repository.supprimer(eleve_2)

connection.close()
