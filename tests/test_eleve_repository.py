import sqlite3
from repositories.eleve_repository import EleveRepository


connection = sqlite3.connect("database/edupaie.db")
repository = EleveRepository(connection)

# Ajouter
eleve_id = repository.ajouter(
    "TEST",
    "Eleve",
    "Terminale",
    "2026-2027",
    150000
)

print("Ajout :", eleve_id)

# Modifier
repository.modifier(
    eleve_id,
    "TEST-MODIFIE",
    "Eleve",
    "Terminale A",
    "2026-2027",
    175000
)

print("Après modification :")
print(repository.lister())

# Supprimer
repository.supprimer(eleve_id)

print("Après suppression :")
print(repository.lister())

connection.close()