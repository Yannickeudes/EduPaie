import sqlite3
from repositories.paiement_repository import PaiementRepository


connection = sqlite3.connect("database/edupaie.db")

paiement_repository = PaiementRepository(connection)

# Création d'un élève de test
cursor = connection.execute(
    """
    INSERT INTO eleves
    (nom, prenom, classe, annee_scolaire, montant_total)
    VALUES (?, ?, ?, ?, ?)
    """,
    ("TEST", "Eleve", "Terminale A", "2026-2027", 200000)
)

eleve_id = cursor.lastrowid
connection.commit()

# Ajouter un paiement
paiement_id = paiement_repository.ajouter(
    "REC-TEST-001",
    eleve_id,
    50000,
    "2026-10-03",
    "Mobile Money"
)

print("Paiement ajouté :", paiement_id)

# Lister tous les paiements
print("\nTous les paiements :")
print(paiement_repository.lister())

# Historique de l'élève
print("\nPaiements de l'élève :")
print(paiement_repository.lister_par_eleve(eleve_id))

# Nettoyage
connection.execute(
    "DELETE FROM paiements WHERE id = ?",
    (paiement_id,)
)

connection.execute(
    "DELETE FROM eleves WHERE id = ?",
    (eleve_id,)
)

connection.commit()
connection.close()