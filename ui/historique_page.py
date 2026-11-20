from PySide6.QtCore import Qt
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

from ui.theme import configurer_tableau


class HistoriquePage(QWidget):
    def __init__(
        self,
        eleve_repository,
        paiement_repository,
        paiement_service,
        recu_service,
        parametres_service
    ):
        super().__init__()

        self.eleve_repository = eleve_repository
        self.paiement_repository = paiement_repository
        self.paiement_service = paiement_service
        self.recu_service = recu_service
        self.parametres_service = parametres_service

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        # Titre
        titre = QLabel("Historique des paiements")
        titre.setObjectName("titre")
        layout.addWidget(titre)

        # Sélection de l'élève
        ligne_selection = QHBoxLayout()
        ligne_selection.setSpacing(10)

        ligne_selection.addWidget(
            QLabel("Élève :")
        )

        self.selection_eleve = QComboBox()
        self.selection_eleve.setMinimumWidth(280)

        self.selection_eleve.currentIndexChanged.connect(
            self.charger_historique
        )

        ligne_selection.addWidget(self.selection_eleve)
        ligne_selection.addStretch()

        self.bouton_actualiser = QPushButton("Actualiser")
        self.bouton_actualiser.setObjectName("secondaire")
        self.bouton_actualiser.clicked.connect(
            self.charger_historique
        )

        ligne_selection.addWidget(self.bouton_actualiser)

        layout.addLayout(ligne_selection)

        # Tableau
        self.tableau = QTableWidget()

        self.tableau.setColumnCount(5)

        self.tableau.setHorizontalHeaderLabels(
            [
                "Date",
                "N° reçu",
                "Montant",
                "Mode",
                "Solde restant"
            ]
        )

        configurer_tableau(self.tableau)
        self.tableau.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        layout.addWidget(self.tableau)

        # Bouton reçu
        zone_boutons = QHBoxLayout()
        zone_boutons.addStretch()

        self.bouton_recu = QPushButton(
            "Ouvrir le reçu"
        )
        self.bouton_recu.setObjectName("primaire")

        self.bouton_recu.clicked.connect(
            self.ouvrir_recu
        )

        zone_boutons.addWidget(self.bouton_recu)

        layout.addLayout(zone_boutons)

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

            valeurs = [
                date_paiement,
                numero_recu,
                f"{montant:,.0f} FCFA",
                mode_paiement,
                f"{solde_restant:,.0f} FCFA"
            ]

            for colonne, valeur in enumerate(valeurs):
                item = QTableWidgetItem(str(valeur))

                # L'ID du paiement est conservé
                # dans les données de la première
                # cellule de chaque ligne.
                if colonne == 0:
                    item.setData(
                        Qt.ItemDataRole.UserRole,
                        paiement_id
                    )

                self.tableau.setItem(
                    ligne,
                    colonne,
                    item
                )

    def ouvrir_recu(self):
        ligne = self.tableau.currentRow()

        if ligne < 0:
            QMessageBox.warning(
                self,
                "Aucun paiement",
                "Sélectionnez un paiement."
            )
            return

        item = self.tableau.item(ligne, 0)

        paiement_id = item.data(Qt.ItemDataRole.UserRole)

        if paiement_id is None:
            QMessageBox.warning(
                self,
                "Erreur",
                "Paiement introuvable."
            )
            return

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
                    solde_restant,
                    self.parametres_service.nom_ecole(),
                    self.parametres_service.chemin_logo(),
                    self.parametres_service.couleur_badge()
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
