import sqlite3
from repositories.eleve_repository import EleveRepository


connection = sqlite3.connect("database/edupaie.db")
repository = EleveRepository(connection)

# Ajout de deux élèves de test
id1 = repository.ajouter(
    "DIALLO",
    "Aminata",
    "Terminale A",
    "2026-2027",
    200000
)

id2 = repository.ajouter(
    "KOFFI",
    "Jean",
    "Première A",
    "2026-2027",
    180000
)

print("Recherche DIALLO :")
print(repository.rechercher("DIALLO"))

print("\nFiltre Terminale A :")
print(repository.rechercher(classe="Terminale A"))

# Nettoyage des données de test
repository.supprimer(id1)
repository.supprimer(id2)

connection.close()