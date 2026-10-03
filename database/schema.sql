CREATE TABLE eleves (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    classe TEXT NOT NULL,
    annee_scolaire TEXT NOT NULL,
    montant_total REAL NOT NULL CHECK(montant_total >= 0)
);

CREATE TABLE paiements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_recu TEXT NOT NULL UNIQUE,
    eleve_id INTEGER NOT NULL,
    montant REAL NOT NULL CHECK(montant > 0),
    date_paiement TEXT NOT NULL,
    mode_paiement TEXT NOT NULL CHECK (
        mode_paiement IN ('Espèces','Chèque','Virement','Mobile Money')
    ),
    solde_apres_paiement REAL NOT NULL CHECK(solde_apres_paiement >= 0),
    FOREIGN KEY (eleve_id) REFERENCES eleves(id)
);