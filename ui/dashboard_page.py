
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem
)


class DashboardPage(QWidget):
    def __init__(self, dashboard_service):
        super().__init__()

        self.dashboard_service = dashboard_service

        layout = QVBoxLayout(self)

        # Titre
        titre = QLabel("Tableau de bord")
        titre.setStyleSheet(
            "font-size: 22px; font-weight: bold;"
        )

        layout.addWidget(titre)

        # Indicateurs
        zone_indicateurs = QHBoxLayout()

        self.label_nombre_eleves = QLabel()
        self.label_total_encaisse = QLabel()
        self.label_total_restant = QLabel()
        self.label_non_soldes = QLabel()

        self.label_nombre_eleves.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )

        self.label_total_encaisse.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )

        self.label_total_restant.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )

        self.label_non_soldes.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )

        zone_indicateurs.addWidget(
            self.label_nombre_eleves
        )

        zone_indicateurs.addWidget(
            self.label_total_encaisse
        )

        zone_indicateurs.addWidget(
            self.label_total_restant
        )

        zone_indicateurs.addWidget(
            self.label_non_soldes
        )

        layout.addLayout(
            zone_indicateurs
        )

        # Filtre par statut
        zone_filtre = QHBoxLayout()

        zone_filtre.addWidget(
            QLabel("Filtrer par statut :")
        )

        self.select_statut = QComboBox()

        self.select_statut.addItems([
            "Tous",
            "Soldé",
            "Partiellement payé",
            "Non payé"
        ])

        self.select_statut.currentIndexChanged.connect(
            self.afficher_eleves
        )

        zone_filtre.addWidget(
            self.select_statut
        )

        self.bouton_actualiser = QPushButton(
            "Actualiser"
        )

        self.bouton_actualiser.clicked.connect(
            self.actualiser
        )

        zone_filtre.addWidget(
            self.bouton_actualiser
        )

        layout.addLayout(
            zone_filtre
        )

        # Tableau
        self.tableau = QTableWidget()

        self.tableau.setColumnCount(7)

        self.tableau.setHorizontalHeaderLabels([
            "Nom",
            "Prénom",
            "Classe",
            "Montant total",
            "Total payé",
            "Solde",
            "Statut"
        ])

        self.tableau.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        layout.addWidget(
            self.tableau
        )

        self.actualiser()

    def actualiser(self):
        nombre_eleves = (
            self.dashboard_service.nombre_eleves()
        )

        total_encaisse = (
            self.dashboard_service.total_encaisse()
        )

        total_restant = (
            self.dashboard_service.total_restant()
        )

        nombre_non_soldes = (
            self.dashboard_service.nombre_non_soldes()
        )

        self.label_nombre_eleves.setText(
            f"Élèves : {nombre_eleves}"
        )

        self.label_total_encaisse.setText(
            f"Encaissé : {total_encaisse:,.0f} FCFA"
        )

        self.label_total_restant.setText(
            f"Restant : {total_restant:,.0f} FCFA"
        )

        self.label_non_soldes.setText(
            f"Non soldés : {nombre_non_soldes}"
        )

        self.afficher_eleves()

    def afficher_eleves(self):
        eleves = (
            self.dashboard_service
            .lister_eleves_avec_statut()
        )

        statut_selectionne = (
            self.select_statut.currentText()
        )

        if statut_selectionne != "Tous":
            eleves = [
                eleve
                for eleve in eleves
                if eleve["statut"] == statut_selectionne
            ]

        self.tableau.setRowCount(0)

        for eleve in eleves:
            ligne = self.tableau.rowCount()

            self.tableau.insertRow(ligne)

            valeurs = [
                eleve["nom"],
                eleve["prenom"],
                eleve["classe"],
                f'{eleve["montant_total"]:,.0f} FCFA',
                f'{eleve["total_paye"]:,.0f} FCFA',
                f'{eleve["solde"]:,.0f} FCFA',
                eleve["statut"]
            ]

            for colonne, valeur in enumerate(valeurs):
                self.tableau.setItem(
                    ligne,
                    colonne,
                    QTableWidgetItem(str(valeur))
                )
