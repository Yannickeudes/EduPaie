import sqlite3


DATABASE = "database/edupaie.db"


def vider_base(connection):
    connection.execute("DELETE FROM paiements")
    connection.execute("DELETE FROM eleves")
    connection.commit()


def ajouter_eleve(
    connection,
    nom,
    prenom,
    classe,
    annee_scolaire,
    montant_total
):
    cursor = connection.execute(
        """
        INSERT INTO eleves
        (
            nom,
            prenom,
            classe,
            annee_scolaire,
            montant_total
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            nom,
            prenom,
            classe,
            annee_scolaire,
            montant_total
        )
    )

    return cursor.lastrowid


def ajouter_paiement(
    connection,
    numero_recu,
    eleve_id,
    montant,
    date_paiement,
    mode_paiement
):
    connection.execute(
        """
        INSERT INTO paiements
        (
            numero_recu,
            eleve_id,
            montant,
            date_paiement,
            mode_paiement
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            numero_recu,
            eleve_id,
            montant,
            date_paiement,
            mode_paiement
        )
    )


def main():
    connection = sqlite3.connect(DATABASE)

    try:
        vider_base(connection)

        eleves = [
            (
                "HONOU",
                "Koffi Karnel",
                "Terminale A",
                "2026-2027",
                150000
            ),
            (
                "KABA",
                "Mariam",
                "Terminale A",
                "2026-2027",
                200000
            ),
            (
                "BENISSAN-TETEVI",
                "Dédé Josepha",
                "Terminale B",
                "2026-2027",
                175000
            ),
            (
                "NABEDE",
                "Gnimdou Yolande",
                "Première A",
                "2026-2027",
                180000
            ),
            (
                "ADIGOU",
                "Adélodjou Félix",
                "Première B",
                "2026-2027",
                160000
            ),
            (
                "MADJRI",
                "Assabah Merveille",
                "Seconde A",
                "2026-2027",
                140000
            ),
            (
                "NAZA",
                "Komla Charbel",
                "Seconde B",
                "2026-2027",
                145000
            ),
            (
                "TCHASSSIM",
                "Eninam Grace",
                "Terminale A",
                "2026-2027",
                210000
            ),
            (
                "CAMARA",
                "Guy Mari Mohamed",
                "Première A",
                "2026-2027",
                155000
            ),
            (
                "EZIMORA",
                "Chioma",
                "Terminale B",
                "2026-2027",
                190000
            ),
            (
                "BLEOUSSI",
                "Ededa",
                "Seconde A",
                "2026-2027",
                135000
            ),
            (
                "AGBAKU",
                "Shine Winner",
                "Première B",
                "2026-2027",
                170000
            ),
            (
                "LAWSON ADJANYRAKU",
                "Nadou Glorie",
                "Terminale A",
                "2026-2027",
                220000
            ),
            (
                "TOSSOUKPE",
                "Claire",
                "Seconde B",
                "2026-2027",
                125000
            ),
            (
                "KOTOKO",
                "Bénédicte",
                "Première A",
                "2026-2027",
                165000
            )
        ]

        ids = []

        for eleve in eleves:
            eleve_id = ajouter_eleve(
                connection,
                *eleve
            )

            ids.append(eleve_id)

        paiements = [
            # HONOU Koffi Kaleb - Soldé
            (
                "REC-2026-0001",
                ids[0],
                150000,
                "2026-09-01",
                "Mobile Money"
            ),

            # KABA Mariam - Partiellement payé
            (
                "REC-2026-0002",
                ids[1],
                100000,
                "2026-09-02",
                "Espèces"
            ),
            (
                "REC-2026-0003",
                ids[1],
                50000,
                "2026-09-15",
                "Mobile Money"
            ),

            # BENISSAN-TETEVI Dédé Josepha - Non payé
            # Aucun paiement

            # NABEDE Gnimdou Yolande - Soldé
            (
                "REC-2026-0004",
                ids[3],
                100000,
                "2026-09-03",
                "Virement"
            ),
            (
                "REC-2026-0005",
                ids[3],
                80000,
                "2026-09-20",
                "Chèque"
            ),

            # ADJIGOU Adélodjou Félix - Partiellement payé
            (
                "REC-2026-0006",
                ids[4],
                60000,
                "2026-09-04",
                "Espèces"
            ),

            # MADJRI Assabah Merveille - Soldé
            (
                "REC-2026-0007",
                ids[5],
                140000,
                "2026-09-05",
                "Mobile Money"
            ),

            # NAZA Komla Charbel - Partiellement payé
            (
                "REC-2026-0008",
                ids[6],
                50000,
                "2026-09-06",
                "Virement"
            ),
            (
                "REC-2026-0009",
                ids[6],
                25000,
                "2026-09-18",
                "Espèces"
            ),

            # TCHASSIM Eninam Grace - Non payé
            # Aucun paiement

            # CAMARA Guy Mari Mohamed - Soldé
            (
                "REC-2026-0010",
                ids[8],
                155000,
                "2026-09-07",
                "Chèque"
            ),

            # EZIMORA Chioma - Partiellement payé
            (
                "REC-2026-0011",
                ids[9],
                90000,
                "2026-09-08",
                "Mobile Money"
            ),

            # BLEOUSSI Ededa - Soldé
            (
                "REC-2026-0012",
                ids[10],
                70000,
                "2026-09-09",
                "Espèces"
            ),
            (
                "REC-2026-0013",
                ids[10],
                65000,
                "2026-09-22",
                "Virement"
            ),

            # AGBAKU Shine Winner - Partiellement payé
            (
                "REC-2026-0014",
                ids[11],
                100000,
                "2026-09-10",
                "Mobile Money"
            ),

            # LAWSON-ADJANYRAKU Nadou Glorie - Non payé
            # Aucun paiement

            # TOSSOUKPE Claire - Soldé
            (
                "REC-2026-0015",
                ids[13],
                125000,
                "2026-09-11",
                "Espèces"
            ),

            # KOTOKO Bénédicte - Partiellement payé
            (
                "REC-2026-0016",
                ids[14],
                80000,
                "2026-09-12",
                "Virement"
            )
        ]

        for paiement in paiements:
            ajouter_paiement(
                connection,
                *paiement
            )

        connection.commit()

        print("Données de démonstration ajoutées avec succès.")
        print(f"Nombre d'élèves : {len(ids)}")
        print(
            f"Nombre de paiements : {len(paiements)}"
        )

    finally:
        connection.close()


if __name__ == "__main__":
    main()
