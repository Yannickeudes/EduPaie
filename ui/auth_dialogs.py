from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QVBoxLayout
)

from services.auth_service import ROLES


class ConfigurationComptesDialog(QDialog):
    def __init__(self, auth_service, parent=None):
        super().__init__(parent)

        self.auth_service = auth_service
        self.mots_de_passe = {}

        self.setWindowTitle("Configuration initiale")
        self.setMinimumWidth(420)

        layout = QVBoxLayout(self)

        titre = QLabel(
            "Choisissez un mot de passe pour chaque poste."
        )
        titre.setStyleSheet("font-weight: 600;")

        layout.addWidget(titre)

        layout.addWidget(
            QLabel(
                "Mot de passe : 4 caractères minimum."
            )
        )

        formulaire = QFormLayout()

        self.champs = {}

        for role in ROLES:
            champ = QLineEdit()
            champ.setEchoMode(
                QLineEdit.EchoMode.Password
            )

            formulaire.addRow(f"{role} :", champ)
            self.champs[role] = champ

        layout.addLayout(formulaire)

        boutons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )

        boutons.accepted.connect(self.enregistrer)
        boutons.rejected.connect(self.reject)

        boutons.button(
            QDialogButtonBox.StandardButton.Save
        ).setText("Enregistrer")

        layout.addWidget(boutons)

    def enregistrer(self):
        mots_de_passe = {}

        for role, champ in self.champs.items():
            mots_de_passe[role] = champ.text()

        try:
            self.auth_service.configurer_comptes(
                mots_de_passe
            )
        except ValueError as erreur:
            QMessageBox.warning(
                self,
                "Configuration",
                str(erreur)
            )
            return

        self.accept()


class LoginDialog(QDialog):
    def __init__(self, auth_service, parent=None):
        super().__init__(parent)

        self.auth_service = auth_service
        self.utilisateur = None

        self.setWindowTitle("Connexion")
        self.setMinimumWidth(360)

        layout = QVBoxLayout(self)

        titre = QLabel("EduPaie")
        titre.setStyleSheet(
            "font-size: 22px; font-weight: 700;"
        )
        titre.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(titre)

        layout.addWidget(
            QLabel("Connectez-vous pour continuer.")
        )

        formulaire = QFormLayout()

        self.select_role = self._creer_combo_roles()
        self.champ_mot_de_passe = QLineEdit()
        self.champ_mot_de_passe.setEchoMode(
            QLineEdit.EchoMode.Password
        )
        self.champ_mot_de_passe.returnPressed.connect(
            self.connexion
        )

        formulaire.addRow("Compte :", self.select_role)
        formulaire.addRow(
            "Mot de passe :",
            self.champ_mot_de_passe
        )

        layout.addLayout(formulaire)

        boutons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )

        boutons.accepted.connect(self.connexion)
        boutons.rejected.connect(self.reject)

        boutons.button(
            QDialogButtonBox.StandardButton.Ok
        ).setText("Se connecter")

        layout.addWidget(boutons)

    def _creer_combo_roles(self):
        combo = QComboBox()
        combo.addItems(ROLES)
        return combo

    def connexion(self):
        role = self.select_role.currentText()
        mot_de_passe = self.champ_mot_de_passe.text()

        if not mot_de_passe:
            QMessageBox.warning(
                self,
                "Connexion",
                "Veuillez saisir votre mot de passe."
            )
            return

        if not self.auth_service.verifier(
            role,
            mot_de_passe
        ):
            QMessageBox.warning(
                self,
                "Connexion",
                "Mot de passe incorrect."
            )
            self.champ_mot_de_passe.clear()
            self.champ_mot_de_passe.setFocus()
            return

        self.utilisateur = role
        self.accept()
