from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QMessageBox
)


class HistoriquePage(QWidget):
    def __init__(
        self,
        eleve_repository,
        paiement_repository,
        paiement_service,
        recu_service
    ):
        super().__init__()

        self.eleve_repository = eleve_repository
        self.paiement_repository = paiement_repository
        self.paiement_service = paiement_service
        self.recu_service = recu_service

        self.setWindowTitle("Historique des paiements")

        layout = QVBoxLayout()

        titre = QLabel("Historique des paiements")
        titre.setStyleSheet(
            "font-size: 20px; font-weight: bold;"
        )
        layout.addWidget(titre)

        ligne_selection = QHBoxLayout()

        label_eleve = QLabel("Élève :")

        self.selection_eleve = QComboBox()

        self.selection_eleve.currentIndexChanged.connect(
            self.charger_historique
        )

        ligne_selection.addWidget(label_eleve)
        ligne_selection.addWidget(
            self.selection_eleve
        )

        layout.addLayout(ligne_selection)

        self.tableau = QTableWidget()

        self.tableau.setColumnCount(7)

        self.tableau.setHorizontalHeaderLabels(
            [
                "Date",
                "N° reçu",
                "Montant",
                "Mode",
                "Solde restant",
                "ID paiement",
                "Élève"
            ]
        )

        self.tableau.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.tableau.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        layout.addWidget(self.tableau)

        self.bouton_recu = QPushButton(
            "Ouvrir le reçu"
        )

        self.bouton_recu.clicked.connect(
            self.ouvrir_recu
        )

        layout.addWidget(self.bouton_recu)

        self.setLayout(layout)

        self.charger_eleves()

    def charger_eleves(self):
        self.selection_eleve.clear()

        eleves = self.eleve_repository.lister()

        self.selection_eleve.addItem(
            "Sélectionner un élève",
            None
        )

        for eleve in eleves:
            eleve_id = eleve[0]
            nom = eleve[1]
            prenom = eleve[2]
            classe = eleve[3]

            texte = (
                f"{nom} {prenom} - {classe}"
            )

            self.selection_eleve.addItem(
                texte,
                eleve_id
            )

        self.tableau.setRowCount(0)

    def charger_historique(self):
        eleve_id = (
            self.selection_eleve.currentData()
        )

        self.tableau.setRowCount(0)

        if eleve_id is None:
            return

        paiements = (
            self.paiement_repository
            .lister_par_eleve(eleve_id)
        )

        eleve = (
            self.eleve_repository
            .trouver_par_id(eleve_id)
        )

        if eleve is None:
            return

        self.tableau.setRowCount(
            len(paiements)
        )

        for ligne, paiement in enumerate(
            paiements
        ):
            paiement_id = paiement[0]
            numero_recu = paiement[1]
            montant = paiement[3]
            date_paiement = paiement[4]
            mode_paiement = paiement[5]

            solde_restant = (
                self.paiement_service
                .calculer_solde_apres_paiement(
                    paiement_id
                )
            )

            self.tableau.setItem(
                ligne,
                0,
                QTableWidgetItem(
                    date_paiement
                )
            )

            self.tableau.setItem(
                ligne,
                1,
                QTableWidgetItem(
                    numero_recu
                )
            )

            self.tableau.setItem(
                ligne,
                2,
                QTableWidgetItem(
                    f"{montant:,.0f} FCFA"
                )
            )

            self.tableau.setItem(
                ligne,
                3,
                QTableWidgetItem(
                    mode_paiement
                )
            )

            self.tableau.setItem(
                ligne,
                4,
                QTableWidgetItem(
                    f"{solde_restant:,.0f} FCFA"
                )
            )

            self.tableau.setItem(
                ligne,
                5,
                QTableWidgetItem(
                    str(paiement_id)
                )
            )

            self.tableau.setItem(
                ligne,
                6,
                QTableWidgetItem(
                    f"{eleve[1]} {eleve[2]}"
                )
            )

        self.tableau.hideColumn(5)
        self.tableau.hideColumn(6)

        self.tableau.resizeColumnsToContents()

    def ouvrir_recu(self):
        ligne = self.tableau.currentRow()

        if ligne < 0:
            QMessageBox.warning(
                self,
                "Aucun paiement",
                "Sélectionnez un paiement."
            )
            return

        paiement_id = int(
            self.tableau.item(
                ligne,
                5
            ).text()
        )

        paiement = (
            self.paiement_repository
            .trouver_par_id(paiement_id)
        )

        if paiement is None:
            QMessageBox.warning(
                self,
                "Erreur",
                "Paiement introuvable."
            )
            return

        eleve_id = paiement[2]

        eleve = (
            self.eleve_repository
            .trouver_par_id(eleve_id)
        )

        if eleve is None:
            QMessageBox.warning(
                self,
                "Erreur",
                "Élève introuvable."
            )
            return

        solde_restant = (
            self.paiement_service
            .calculer_solde_apres_paiement(
                paiement_id
            )
        )

        try:
            chemin = (
                self.recu_service.generer_recu(
                    paiement[1],
                    eleve,
                    paiement[3],
                    paiement[4],
                    paiement[5],
                    solde_restant
                )
            )

            QMessageBox.information(
                self,
                "Reçu généré",
                f"Le reçu a été généré ici :\n{chemin}"
            )

        except Exception as erreur:
            QMessageBox.critical(
                self,
                "Erreur",
                f"Impossible de générer le reçu :\n{erreur}"
            )