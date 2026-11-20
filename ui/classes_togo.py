# Classes du système éducatif togolais
CLASSES_TOGO = [
    # Maternelle
    "Maternelle 1",
    "Maternelle 2",
    # Primaire
    "CP1",
    "CP2",
    "CE1",
    "CE2",
    "CM1",
    "CM2",
    # Collège
    "6ème",
    "5ème",
    "4ème",
    "3ème",
]

# Lycée moderne : séries A4, C et D
for niveau in ("Seconde", "Première", "Terminale"):
    for serie in ("A4", "C", "D"):
        CLASSES_TOGO.append(f"{niveau} {serie}")

# Lycée technique : séries G1, G2, G3, F1, F2, F3, F4, Ti et E
for niveau in ("Seconde", "Première", "Terminale"):
    for serie in ("G1", "G2", "G3", "F1", "F2", "F3", "F4", "Ti", "E"):
        CLASSES_TOGO.append(f"{niveau} {serie}")
