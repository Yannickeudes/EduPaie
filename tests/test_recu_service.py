from services.recu_service import RecuService


service = RecuService()

eleve = (
    1,
    "DIALLO",
    "Aminata",
    "Terminale A",
    "2026-2027",
    200000
)

chemin = service.generer_recu(
    "REC-TEST-PDF-001",
    eleve,
    50000,
    "2026-10-03",
    "Mobile Money",
    150000
)

print("Reçu généré :", chemin)