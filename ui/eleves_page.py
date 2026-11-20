from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QFrame,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QDoubleSpinBox
)

from ui.theme import configurer_tableau
from ui.classes_togo import CLASSES_TOGO


class ElevesPage(QWidget):
    def __init__(
        self,
        eleve_repository,
        eleve_service
    ):
        super().__init__()

        self.eleve_repository = eleve_repository
        self.eleve_service = eleve_service

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        # Titre
        titre = QLabel("Gestion des élèves")
        titre.setObjectName("titre")

        layout.addWidget(titre)

        # Formulaire
        carte_formulaire = QFrame()
        carte_formulaire.setObjectName("carte")

        layout_carte = QVBoxLayout(carte_formulaire)
        layout_carte.setContentsMargins(16, 16, 16, 16)

        formulaire = QFormLayout()

        self.champ_nom = QLineEdit()
        self.champ_prenom = QLineEdit()
        self.champ_classe = QComboBox()
        self.champ_classe.setEditable(True)
        self.champ_classe.addItems(CLASSES_TOGO)
        self.champ_annee = QLineEdit()

        self.champ_montant = QDoubleSpinBox()
        self.champ_montant.setMaximum(100000000)
        self.champ_montant.setDecimals(0)
        self.champ_montant.setSuffix(" FCFA")

        formulaire.addRow(
            "Nom :",
            self.champ_nom
        )

        formulaire.addRow(
            "Prénom :",
            self.champ_prenom
        )

        formulaire.addRow(
            "Classe :",
            self.champ_classe
        )

        formulaire.addRow(
            "Année scolaire :",
            self.champ_annee
        )

        formulaire.addRow(
            "Montant total :",
            self.champ_montant
        )

        layout_carte.addLayout(formulaire)

        # Bouton ajout
        self.bouton_ajouter = QPushButton(
            "Ajouter l'élève"
        )
        self.bouton_ajouter.setObjectName("primaire")

        self.bouton_ajouter.clicked.connect(
            self.ajouter_eleve
        )

        layout_carte.addWidget(
            self.bouton_ajouter
        )

        layout.addWidget(carte_formulaire)

        # Recherche
        zone_recherche = QHBoxLayout()

        self.champ_recherche = QLineEdit()

        self.champ_recherche.setPlaceholderText(
            "Rechercher par nom, prénom ou classe..."
        )

        self.champ_recherche.returnPressed.connect(
            self.rechercher_eleves
        )

        self.bouton_rechercher = QPushButton(
            "Rechercher"
        )
        self.bouton_rechercher.setObjectName("primaire")

        self.bouton_rechercher.clicked.connect(
            self.rechercher_eleves
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

        # Filtre par classe
        zone_filtre = QHBoxLayout()

        self.champ_filtre_classe = QLineEdit()

        self.champ_filtre_classe.setPlaceholderText(
            "Exemple : Terminale A"
        )

        self.champ_filtre_classe.returnPressed.connect(
            self.filtrer_par_classe
        )

        self.bouton_filtrer = QPushButton(
            "Filtrer par classe"
        )
        self.bouton_filtrer.setObjectName("secondaire")

        self.bouton_filtrer.clicked.connect(
            self.filtrer_par_classe
        )

        self.bouton_toutes_classes = QPushButton(
            "Toutes les classes"
        )
        self.bouton_toutes_classes.setObjectName("secondaire")

        self.bouton_toutes_classes.clicked.connect(
            self.charger_eleves
        )

        zone_filtre.addWidget(
            self.champ_filtre_classe
        )

        zone_filtre.addWidget(
            self.bouton_filtrer
        )

        zone_filtre.addWidget(
            self.bouton_toutes_classes
        )

        layout.addLayout(
            zone_filtre
        )

        # Tableau
        self.tableau = QTableWidget()

        self.tableau.setColumnCount(6)

        self.tableau.setHorizontalHeaderLabels([
            "ID",
            "Nom",
            "Prénom",
            "Classe",
            "Année scolaire",
            "Montant total"
        ])

        self.tableau.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        configurer_tableau(self.tableau)

        self.tableau.itemSelectionChanged.connect(
            self.charger_eleve_selectionne
        )

        self.label_compteur = QLabel("")
        self.label_compteur.setStyleSheet(
            "color: #64748B; font-size: 12px;"
        )

        layout.addWidget(self.label_compteur)

        layout.addWidget(
            self.tableau
        )

        # Boutons
        zone_boutons = QHBoxLayout()

        self.bouton_actualiser = QPushButton(
            "Actualiser"
        )
        self.bouton_actualiser.setObjectName("secondaire")

        self.bouton_actualiser.clicked.connect(
            self.charger_eleves
        )

        self.bouton_modifier = QPushButton(
            "Modifier"
        )
        self.bouton_modifier.setObjectName("secondaire")

        self.bouton_modifier.clicked.connect(
            self.modifier_eleve
        )

        self.bouton_supprimer = QPushButton(
            "Supprimer"
        )
        self.bouton_supprimer.setObjectName("danger")

        self.bouton_supprimer.clicked.connect(
            self.supprimer_eleve
        )

        zone_boutons.addWidget(
            self.bouton_actualiser
        )

        zone_boutons.addWidget(
            self.bouton_modifier
        )

        zone_boutons.addWidget(
            self.bouton_supprimer
        )

        layout.addLayout(
            zone_boutons
        )

        self.charger_eleves()

    def ajouter_eleve(self):
        nom = self.champ_nom.text().strip()
        prenom = self.champ_prenom.text().strip()
        classe = self.champ_classe.text().strip()
        annee = self.champ_annee.text().strip()
        montant = self.champ_montant.value()

        if not nom or not prenom or not classe or not annee:
            QMessageBox.warning(
                self,
                "Validation",
                "Veuillez remplir tous les champs."
            )
            return

        if montant <= 0:
            QMessageBox.warning(
                self,
                "Validation",
                "Le montant total doit être supérieur à 0."
            )
            return

        self.eleve_repository.ajouter(
            nom,
            prenom,
            classe,
            annee,
            montant
        )

        QMessageBox.information(
            self,
            "Succès",
            "L'élève a été ajouté avec succès."
        )

        self.vider_formulaire()
        self.charger_eleves()

    def charger_eleves(self):
        eleves = self.eleve_repository.lister()

        self.afficher_eleves(
            eleves
        )

    def rechercher_eleves(self):
        recherche = (
            self.champ_recherche
            .text()
            .strip()
        )

        eleves = self.eleve_repository.rechercher(
            recherche=recherche
        )

        self.afficher_eleves(
            eleves
        )

    def filtrer_par_classe(self):
        classe = (
            self.champ_filtre_classe
            .text()
            .strip()
        )

        if not classe:
            QMessageBox.warning(
                self,
                "Validation",
                "Veuillez saisir une classe."
            )
            return

        eleves = self.eleve_repository.rechercher(
            classe=classe
        )

        self.afficher_eleves(
            eleves
        )

    def afficher_eleves(self, eleves):
        self.tableau.blockSignals(True)

        self.tableau.setRowCount(0)

        for eleve in eleves:
            ligne = self.tableau.rowCount()

            self.tableau.insertRow(
                ligne
            )

            for colonne, valeur in enumerate(eleve):
                self.tableau.setItem(
                    ligne,
                    colonne,
                    QTableWidgetItem(
                        str(valeur)
                    )
                )

        self.tableau.blockSignals(False)

        nombre = len(eleves)
        self.label_compteur.setText(
            f"{nombre} élève{'s' if nombre > 1 else ''}"
        )

    def charger_eleve_selectionne(self):
        ligne = self.tableau.currentRow()

        if ligne < 0:
            return

        self.champ_nom.setText(
            self.tableau.item(
                ligne,
                1
            ).text()
        )

        self.champ_prenom.setText(
            self.tableau.item(
                ligne,
                2
            ).text()
        )

        self.champ_classe.setCurrentText(
            self.tableau.item(
                ligne,
                3
            ).text()
        )

        self.champ_annee.setText(
            self.tableau.item(
                ligne,
                4
            ).text()
        )

        montant = float(
            self.tableau.item(
                ligne,
                5
            ).text()
        )

        self.champ_montant.setValue(
            montant
        )

    def modifier_eleve(self):
        ligne = self.tableau.currentRow()

        if ligne < 0:
            QMessageBox.warning(
                self,
                "Attention",
                "Sélectionnez un élève."
            )
            return

        eleve_id = int(
            self.tableau.item(
                ligne,
                0
            ).text()
        )

        nom = self.champ_nom.text().strip()
        prenom = self.champ_prenom.text().strip()
        classe = self.champ_classe.text().strip()
        annee = self.champ_annee.text().strip()
        montant = self.champ_montant.value()

        try:
            self.eleve_service.modifier_eleve(
                eleve_id,
                nom,
                prenom,
                classe,
                annee,
                montant
            )

            QMessageBox.information(
                self,
                "Succès",
                "L'élève a été modifié avec succès."
            )

            self.charger_eleves()

        except ValueError as erreur:
            QMessageBox.warning(
                self,
                "Modification refusée",
                str(erreur)
            )

    def supprimer_eleve(self):
        ligne = self.tableau.currentRow()

        if ligne < 0:
            QMessageBox.warning(
                self,
                "Attention",
                "Sélectionnez un élève."
            )
            return

        eleve_id = int(
            self.tableau.item(
                ligne,
                0
            ).text()
        )

        confirmation = QMessageBox.question(
            self,
            "Confirmation",
            "Voulez-vous vraiment supprimer cet élève ?"
        )

        if confirmation != QMessageBox.StandardButton.Yes:
            return

        try:
            self.eleve_service.supprimer_eleve(
                eleve_id
            )

            QMessageBox.information(
                self,
                "Succès",
                "L'élève a été supprimé avec succès."
            )

            self.vider_formulaire()
            self.charger_eleves()

        except ValueError as erreur:
            QMessageBox.warning(
                self,
                "Suppression refusée",
                str(erreur)
            )

    def vider_formulaire(self):
        self.champ_nom.clear()
        self.champ_prenom.clear()
        self.champ_classe.setCurrentText("")
        self.champ_annee.clear()
        self.champ_montant.setValue(0)