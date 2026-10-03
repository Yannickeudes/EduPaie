
import os

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox
)

from services.recu_service import RecuService


class HistoriquePage(QWidget):
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
        titre = QLabel("Historique des paiements")
        titre.setStyleSheet(
            "font-size: 22px; font-weight: bold;"
        )

        layout.addWidget(titre)

        # Sélection de l'élève
        zone_selection = QHBoxLayout()

        zone_selection.addWidget(
            QLabel("Élève :")
        )

        self.select_eleve = QComboBox()

        self.select_eleve.currentIndexChanged.connect(
            self.charger_historique
        )

        zone_selection.addWidget(
            self.select_eleve
        )

        layout.addLayout(
            zone_selection
        )

        # Tableau
        self.tableau = QTableWidget()
        self.tableau.setColumnCount(5)

        self.tableau.setHorizontalHeaderLabels([
            "N° reçu",
            "Montant",
            "Date",
            "Mode de paiement",
            "ID paiement"
        ])

        self.tableau.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        layout.addWidget(self.tableau)

        # Boutons
        zone_boutons = QHBoxLayout()

        self.bouton_actualiser = QPushButton(
            "Actualiser"
        )

        self.bouton_actualiser.clicked.connect(
            self.charger_eleves
        )

        self.bouton_ouvrir_recu = QPushButton(
            "Ouvrir le reçu"
        )

        self.bouton_ouvrir_recu.clicked.connect(
            self.ouvrir_recu
        )

        zone_boutons.addWidget(
            self.bouton_actualiser
        )

        zone_boutons.addWidget(
            self.bouton_ouvrir_recu
        )

        layout.addLayout(
            zone_boutons
        )

        self.charger_eleves()

    def charger_eleves(self):
        self.select_eleve.blockSignals(True)
        self.select_eleve.clear()

        eleves = self.eleve_repository.lister()

        for eleve in eleves:
            eleve_id = eleve[0]
            nom = eleve[1]
            prenom = eleve[2]
            classe = eleve[3]

            texte = (
                f"{nom} {prenom} - {classe}"
            )

            self.select_eleve.addItem(
                texte,
                eleve_id
            )

        self.select_eleve.blockSignals(False)

        self.charger_historique()

    def charger_historique(self):
        eleve_id = self.select_eleve.currentData()

        self.tableau.setRowCount(0)

        if eleve_id is None:
            return

        paiements = (
            self.paiement_repository.lister_par_eleve(
                eleve_id
            )
        )

        for paiement in paiements:
            ligne = self.tableau.rowCount()

            self.tableau.insertRow(ligne)

            self.tableau.setItem(
                ligne,
                0,
                QTableWidgetItem(
                    str(paiement[1])
                )
            )

            self.tableau.setItem(
                ligne,
                1,
                QTableWidgetItem(
                    f"{paiement[3]:,.0f} FCFA"
                )
            )

            self.tableau.setItem(
                ligne,
                2,
                QTableWidgetItem(
                    str(paiement[4])
                )
            )

            self.tableau.setItem(
                ligne,
                3,
                QTableWidgetItem(
                    str(paiement[5])
                )
            )

            self.tableau.setItem(
                ligne,
                4,
                QTableWidgetItem(
                    str(paiement[0])
                )
            )

    def ouvrir_recu(self):
        ligne = self.tableau.currentRow()

        if ligne < 0:
            QMessageBox.warning(
                self,
                "Attention",
                "Sélectionnez un paiement."
            )
            return

        numero_recu = (
            self.tableau.item(ligne, 0).text()
        )

        paiement = (
            self.paiement_repository
            .trouver_par_numero_recu(numero_recu)
        )

        if paiement is None:
            QMessageBox.warning(
                self,
                "Erreur",
                "Paiement introuvable."
            )
            return

        eleve_id = paiement[2]

        eleve = self.eleve_repository.trouver_par_id(
            eleve_id
        )

        if eleve is None:
            QMessageBox.warning(
                self,
                "Erreur",
                "Élève introuvable."
            )
            return

        solde_restant = (
            self.paiement_service.calculer_solde(
                eleve_id
            )
        )

        chemin = self.recu_service.generer_recu(
            paiement[1],
            eleve,
            paiement[3],
            paiement[4],
            paiement[5],
            solde_restant
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
