import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPixmap
from PySide6.QtWidgets import (
    QColorDialog,
    QFileDialog,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget
)


class ParametresPage(QWidget):
    def __init__(
        self,
        parametres_service,
        auth_service=None,
        utilisateur="",
        on_change=None
    ):
        super().__init__()

        self.parametres_service = parametres_service
        self.auth_service = auth_service
        self.utilisateur = utilisateur
        self.on_change = on_change
        self.chemin_logo_choisi = None
        self.couleur_choisie = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        # Titre
        titre = QLabel("Paramètres")
        titre.setObjectName("titre")

        layout.addWidget(titre)

        # Carte des paramètres
        carte = QFrame()
        carte.setObjectName("carte")

        layout_carte = QVBoxLayout(carte)
        layout_carte.setContentsMargins(16, 16, 16, 16)
        layout_carte.setSpacing(14)

        formulaire = QFormLayout()

        self.champ_nom_ecole = QLineEdit()
        self.champ_nom_ecole.setPlaceholderText(
            "Exemple : Collège Les Palmiers"
        )

        formulaire.addRow(
            "Nom de l'établissement :",
            self.champ_nom_ecole
        )

        layout_carte.addLayout(formulaire)

        # Logo
        label_logo_titre = QLabel("Logo de l'établissement :")
        label_logo_titre.setStyleSheet("font-weight: 600;")

        layout_carte.addWidget(label_logo_titre)

        zone_logo = QHBoxLayout()
        zone_logo.setSpacing(16)

        self.label_apercu_logo = QLabel()
        self.label_apercu_logo.setFixedSize(110, 110)
        self.label_apercu_logo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.label_apercu_logo.setStyleSheet(
            "border: 1px dashed #CBD5E1; border-radius: 10px;"
            " background-color: #F8FAFC; color: #94A3B8;"
        )
        self.label_apercu_logo.setText("Aucun logo")

        zone_boutons_logo = QVBoxLayout()
        zone_boutons_logo.setSpacing(8)

        self.bouton_choisir_logo = QPushButton(
            "Choisir un logo..."
        )
        self.bouton_choisir_logo.setObjectName("secondaire")
        self.bouton_choisir_logo.clicked.connect(
            self.choisir_logo
        )

        self.bouton_supprimer_logo = QPushButton(
            "Supprimer le logo"
        )
        self.bouton_supprimer_logo.setObjectName("danger")
        self.bouton_supprimer_logo.clicked.connect(
            self.supprimer_logo
        )

        zone_boutons_logo.addWidget(
            self.bouton_choisir_logo
        )
        zone_boutons_logo.addWidget(
            self.bouton_supprimer_logo
        )
        zone_boutons_logo.addStretch()

        zone_logo.addWidget(self.label_apercu_logo)
        zone_logo.addLayout(zone_boutons_logo)
        zone_logo.addStretch()

        layout_carte.addLayout(zone_logo)

        # Couleur de la marque
        zone_couleur = QHBoxLayout()
        zone_couleur.setSpacing(10)

        zone_couleur.addWidget(
            QLabel("Couleur de la marque :")
        )

        self.bouton_couleur = QPushButton("Choisir...")
        self.bouton_couleur.setObjectName("secondaire")
        self.bouton_couleur.setFixedWidth(110)
        self.bouton_couleur.clicked.connect(
            self.choisir_couleur
        )

        zone_couleur.addWidget(self.bouton_couleur)
        zone_couleur.addStretch()

        layout_carte.addLayout(zone_couleur)

        # Bouton enregistrer
        zone_actions = QHBoxLayout()
        zone_actions.addStretch()

        self.bouton_enregistrer = QPushButton(
            "Enregistrer les paramètres"
        )
        self.bouton_enregistrer.setObjectName("primaire")
        self.bouton_enregistrer.clicked.connect(
            self.enregistrer
        )

        zone_actions.addWidget(self.bouton_enregistrer)

        layout_carte.addLayout(zone_actions)

        layout.addWidget(carte)

        # Carte sécurité : changement de mot de passe
        if self.auth_service is not None:
            self._construire_carte_securite(layout)

        layout.addStretch()

        self.charger_parametres()

    def _construire_carte_securite(self, layout):
        carte_securite = QFrame()
        carte_securite.setObjectName("carte")

        layout_carte = QVBoxLayout(carte_securite)
        layout_carte.setContentsMargins(16, 16, 16, 16)
        layout_carte.setSpacing(12)

        titre_securite = QLabel("Sécurité")
        titre_securite.setStyleSheet("font-weight: 600;")

        layout_carte.addWidget(titre_securite)

        layout_carte.addWidget(
            QLabel(
                f"Compte connecté : {self.utilisateur}"
            )
        )

        formulaire = QFormLayout()

        self.champ_mdp_actuel = QLineEdit()
        self.champ_mdp_actuel.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        self.champ_nouveau_mdp = QLineEdit()
        self.champ_nouveau_mdp.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        self.champ_confirmation_mdp = QLineEdit()
        self.champ_confirmation_mdp.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        formulaire.addRow(
            "Mot de passe actuel :",
            self.champ_mdp_actuel
        )
        formulaire.addRow(
            "Nouveau mot de passe :",
            self.champ_nouveau_mdp
        )
        formulaire.addRow(
            "Confirmer :",
            self.champ_confirmation_mdp
        )

        layout_carte.addLayout(formulaire)

        self.bouton_changer_mdp = QPushButton(
            "Changer le mot de passe"
        )
        self.bouton_changer_mdp.setObjectName("secondaire")
        self.bouton_changer_mdp.clicked.connect(
            self.changer_mot_de_passe
        )

        layout_carte.addWidget(
            self.bouton_changer_mdp
        )

        layout.addWidget(carte_securite)

    def changer_mot_de_passe(self):
        ancien = self.champ_mdp_actuel.text()
        nouveau = self.champ_nouveau_mdp.text()
        confirmation = self.champ_confirmation_mdp.text()

        if nouveau != confirmation:
            QMessageBox.warning(
                self,
                "Mot de passe",
                "Les deux nouveaux mots de passe "
                "ne correspondent pas."
            )
            return

        try:
            self.auth_service.changer_mot_de_passe(
                self.utilisateur,
                ancien,
                nouveau
            )

            self.champ_mdp_actuel.clear()
            self.champ_nouveau_mdp.clear()
            self.champ_confirmation_mdp.clear()

            QMessageBox.information(
                self,
                "Succès",
                "Le mot de passe a été changé "
                "avec succès."
            )

        except ValueError as erreur:
            QMessageBox.warning(
                self,
                "Mot de passe refusé",
                str(erreur)
            )

    def charger_parametres(self):
        self.champ_nom_ecole.setText(
            self.parametres_service.nom_ecole()
        )

        self.chemin_logo_choisi = None
        self.couleur_choisie = None

        self._afficher_apercu(
            self.parametres_service.chemin_logo()
        )

        self._appliquer_couleur(
            self.parametres_service.couleur_badge()
        )

    def _appliquer_couleur(self, couleur):
        self.bouton_couleur.setStyleSheet(
            f"background-color: {couleur};"
            " color: #FFFFFF; font-weight: 600;"
        )
        self.bouton_couleur.setText(couleur)

    def _afficher_apercu(self, chemin):
        if chemin and os.path.exists(chemin):
            pixmap = QPixmap(chemin)

            if not pixmap.isNull():
                self.label_apercu_logo.setPixmap(
                    pixmap.scaled(
                        100,
                        100,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                )
                self.label_apercu_logo.setText("")
                return

        self.label_apercu_logo.setPixmap(QPixmap())
        self.label_apercu_logo.setText("Aucun logo")

    def choisir_logo(self):
        chemin, _ = QFileDialog.getOpenFileName(
            self,
            "Choisir un logo",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif *.ico *.webp)"
        )

        if not chemin:
            return

        self.chemin_logo_choisi = chemin
        self._afficher_apercu(chemin)

    def choisir_couleur(self):
        couleur_actuelle = (
            self.couleur_choisie
            or self.parametres_service.couleur_badge()
        )

        couleur = QColorDialog.getColor(
            QColor(couleur_actuelle),
            self,
            "Couleur de la marque"
        )

        if not couleur.isValid():
            return

        self.couleur_choisie = couleur.name()
        self._appliquer_couleur(self.couleur_choisie)

    def supprimer_logo(self):
        self.chemin_logo_choisi = ""
        self.parametres_service.supprimer_logo()
        self._afficher_apercu(None)

        if self.on_change:
            self.on_change()

        QMessageBox.information(
            self,
            "Logo supprimé",
            "Le logo a été supprimé."
        )

    def enregistrer(self):
        try:
            self.parametres_service.enregistrer(
                self.champ_nom_ecole.text(),
                self.chemin_logo_choisi or None,
                self.couleur_choisie
            )

            self.chemin_logo_choisi = None
            self.couleur_choisie = None

            if self.on_change:
                self.on_change()

            QMessageBox.information(
                self,
                "Succès",
                "Les paramètres ont été enregistrés."
            )

        except ValueError as erreur:
            QMessageBox.warning(
                self,
                "Paramètres invalides",
                str(erreur)
            )
