from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget
)

from ui.theme import (
    COULEUR_ATTENTION,
    COULEUR_DANGER,
    COULEUR_PRIMAIRE,
    COULEUR_SUCCES,
    COULEUR_TEXTE_ATENUE,
    configurer_tableau,
    item_statut
)


class CarteIndicateur(QFrame):
    def __init__(self, libelle, couleur):
        super().__init__()

        self.setObjectName("carte")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(4)

        label_libelle = QLabel(libelle)
        label_libelle.setStyleSheet(
            f"color: {COULEUR_TEXTE_ATENUE}; font-size: 12px;"
        )

        self.label_valeur = QLabel("—")
        self.label_valeur.setStyleSheet(
            f"color: {couleur}; font-size: 22px; font-weight: 700;"
        )

        layout.addWidget(label_libelle)
        layout.addWidget(self.label_valeur)


class DashboardPage(QWidget):
    def __init__(self, dashboard_service):
        super().__init__()

        self.dashboard_service = dashboard_service

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Titre
        titre = QLabel("Tableau de bord")
        titre.setObjectName("titre")

        layout.addWidget(titre)

        # Cartes d'indicateurs
        zone_cartes = QHBoxLayout()
        zone_cartes.setSpacing(16)

        self.carte_eleves = CarteIndicateur(
            "Élèves", COULEUR_PRIMAIRE
        )
        self.carte_encaisse = CarteIndicateur(
            "Total encaissé", COULEUR_SUCCES
        )
        self.carte_restant = CarteIndicateur(
            "Total restant", COULEUR_ATTENTION
        )
        self.carte_non_soldes = CarteIndicateur(
            "Élèves non soldés", COULEUR_DANGER
        )

        for carte in (
            self.carte_eleves,
            self.carte_encaisse,
            self.carte_restant,
            self.carte_non_soldes
        ):
            zone_cartes.addWidget(carte)

        layout.addLayout(zone_cartes)

        # Filtre par statut
        zone_filtre = QHBoxLayout()
        zone_filtre.setSpacing(10)

        zone_filtre.addWidget(
            QLabel("Filtrer par statut :")
        )

        self.select_statut = QComboBox()
        self.select_statut.setMinimumWidth(200)

        self.select_statut.addItems([
            "Tous",
            "Soldé",
            "Partiellement payé",
            "Non payé"
        ])

        self.select_statut.currentIndexChanged.connect(
            self.afficher_eleves
        )

        zone_filtre.addWidget(self.select_statut)
        zone_filtre.addStretch()

        self.bouton_actualiser = QPushButton("Actualiser")
        self.bouton_actualiser.setObjectName("secondaire")

        self.bouton_actualiser.clicked.connect(self.actualiser)

        zone_filtre.addWidget(self.bouton_actualiser)

        layout.addLayout(zone_filtre)

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

        configurer_tableau(self.tableau)
        self.tableau.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        layout.addWidget(self.tableau)

        self.actualiser()

    def actualiser(self):
        nombre_eleves = self.dashboard_service.nombre_eleves()
        total_encaisse = self.dashboard_service.total_encaisse()
        total_restant = self.dashboard_service.total_restant()
        nombre_non_soldes = (
            self.dashboard_service.nombre_non_soldes()
        )

        self.carte_eleves.label_valeur.setText(
            str(nombre_eleves)
        )
        self.carte_encaisse.label_valeur.setText(
            f"{total_encaisse:,.0f} FCFA"
        )
        self.carte_restant.label_valeur.setText(
            f"{total_restant:,.0f} FCFA"
        )
        self.carte_non_soldes.label_valeur.setText(
            str(nombre_non_soldes)
        )

        self.afficher_eleves()

    def afficher_eleves(self):
        eleves = self.dashboard_service.lister_eleves_avec_statut()

        statut_selectionne = self.select_statut.currentText()

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
                item_statut(eleve["statut"])
            ]

            for colonne, valeur in enumerate(valeurs):
                if isinstance(valeur, QTableWidgetItem):
                    self.tableau.setItem(ligne, colonne, valeur)
                else:
                    self.tableau.setItem(
                        ligne,
                        colonne,
                        QTableWidgetItem(str(valeur))
                    )
