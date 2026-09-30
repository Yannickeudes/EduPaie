import sqlite3
from repositories.eleve_repository import EleveRepository


connection = sqlite3.connect("database/edupaie.db")

repository = EleveRepository(connection)

eleve_id = repository.ajouter(
    "APETOH",
    "Yannick",
    "Terminale",
    "2026-2027",
    150000
)

print("Élève ajouté avec l'ID :", eleve_id)

eleves = repository.lister()

for eleve in eleves:
    print(eleve)

connection.close()