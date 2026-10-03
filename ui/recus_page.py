import os

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox
)

from services.recu_service import RecuService


class RecusPage(QWidget):
    def __init__(
        self,
        eleve_repository,
        paiement_repository,
        paiement_service
    ):
        super().__init__()

        self.eleve_repository = eleve_repository
        self.paiement_repository = paiement_repository
        self.paiement_service = paiement_service

        self.recu_service = RecuService()

        layout = QVBoxLayout(self)

        # Titre
        titre = QLabel("Gestion des reçus")
        titre.setStyleSheet(
            "font-size: 22px; font-weight: bold;"
        )

        layout.addWidget(titre)

        # Recherche
        zone_recherche = QHBoxLayout()

        self.champ_recherche = QLineEdit()

        self.champ_recherche.setPlaceholderText(
            "Exemple : REC-2026-0001"
        )

        self.bouton_rechercher = QPushButton(
            "Rechercher"
        )

        self.bouton_rechercher.clicked.connect(
            self.rechercher_recu
        )

        zone_recherche.addWidget(
            self.champ_recherche
        )

        zone_recherche.addWidget(
            self.bouton_rechercher
        )

        layout.addLayout(
            zone_recherche
        )

        # Tableau
        self.tableau = QTableWidget()

        self.tableau.setColumnCount(6)

        self.tableau.setHorizontalHeaderLabels([
            "N° reçu",
            "Élève",
            "Montant",
            "Date",
            "Mode",
            "Solde"
        ])

        self.tableau.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        layout.addWidget(
            self.tableau
        )

        # Boutons
        zone_boutons = QHBoxLayout()

        self.bouton_tous = QPushButton(
            "Afficher tous les reçus"
        )

        self.bouton_tous.clicked.connect(
            self.charger_tous_les_recus
        )

        self.bouton_ouvrir = QPushButton(
            "Ouvrir le reçu"
        )

        self.bouton_ouvrir.clicked.connect(
            self.ouvrir_recu
        )

        zone_boutons.addWidget(
            self.bouton_tous
        )

        zone_boutons.addWidget(
            self.bouton_ouvrir
        )

        layout.addLayout(
            zone_boutons
        )

        self.charger_tous_les_recus()

    def charger_tous_les_recus(self):
        paiements = (
            self.paiement_repository.lister()
        )

        self.afficher_paiements(
            paiements
        )

    def rechercher_recu(self):
        numero_recu = (
            self.champ_recherche.text().strip()
        )

        if not numero_recu:
            QMessageBox.warning(
                self,
                "Validation",
                "Veuillez saisir un numéro de reçu."
            )
            return

        paiement = (
            self.paiement_repository
            .trouver_par_numero_recu(numero_recu)
        )

        if paiement is None:
            self.tableau.setRowCount(0)

            QMessageBox.information(
                self,
                "Recherche",
                "Aucun reçu trouvé."
            )

            return

        self.afficher_paiements([
            paiement
        ])

    def afficher_paiements(self, paiements):
        self.tableau.setRowCount(0)

        for paiement in paiements:
            eleve_id = paiement[2]

            eleve = (
                self.eleve_repository
                .trouver_par_id(eleve_id)
            )

            if eleve is None:
                continue

            solde = (
                self.paiement_service
                .calculer_solde(eleve_id)
            )

            ligne = self.tableau.rowCount()

            self.tableau.insertRow(ligne)

            nom_complet = (
                f"{eleve[1]} {eleve[2]}"
            )

            valeurs = [
                paiement[1],
                nom_complet,
                f"{paiement[3]:,.0f} FCFA",
                paiement[4],
                paiement[5],
                f"{solde:,.0f} FCFA"
            ]

            for colonne, valeur in enumerate(
                valeurs
            ):
                self.tableau.setItem(
                    ligne,
                    colonne,
                    QTableWidgetItem(
                        str(valeur)
                    )
                )

    def ouvrir_recu(self):
        ligne = self.tableau.currentRow()

        if ligne < 0:
            QMessageBox.warning(
                self,
                "Attention",
                "Sélectionnez un reçu."
            )
            return

        numero_recu = (
            self.tableau.item(
                ligne,
                0
            ).text()
        )

        paiement = (
            self.paiement_repository
            .trouver_par_numero_recu(
                numero_recu
            )
        )

        if paiement is None:
            QMessageBox.warning(
                self,
                "Erreur",
                "Reçu introuvable."
            )
            return

        eleve = (
            self.eleve_repository
            .trouver_par_id(
                paiement[2]
            )
        )

        if eleve is None:
            QMessageBox.warning(
                self,
                "Erreur",
                "Élève introuvable."
            )
            return

        solde = (
            self.paiement_service
            .calculer_solde(
                paiement[2]
            )
        )

        chemin = (
            self.recu_service.generer_recu(
                paiement[1],
                eleve,
                paiement[3],
                paiement[4],
                paiement[5],
                solde
            )
        )

        try:
            os.startfile(
                os.path.abspath(chemin)
            )

        except Exception as erreur:
            QMessageBox.warning(
                self,
                "Erreur",
                f"Impossible d'ouvrir le reçu.\n\n{erreur}"
            )
