from datetime import date

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QFrame,
    QLabel,
    QComboBox,
    QDoubleSpinBox,
    QDateEdit,
    QPushButton,
    QMessageBox
)

from ui.theme import COULEUR_DANGER, COULEUR_SUCCES, COULEUR_TEXTE_ATENUE


class PaiementsPage(QWidget):
    def __init__(
        self,
        eleve_repository,
        paiement_service
    ):
        super().__init__()

        self.eleve_repository = eleve_repository
        self.paiement_service = paiement_service

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        titre = QLabel("Enregistrement des paiements")
        titre.setObjectName("titre")

        layout.addWidget(titre)

        carte_formulaire = QFrame()
        carte_formulaire.setObjectName("carte")

        layout_carte = QVBoxLayout(carte_formulaire)
        layout_carte.setContentsMargins(16, 16, 16, 16)

        formulaire = QFormLayout()

        # Élève
        self.select_eleve = QComboBox()

        self.select_eleve.currentIndexChanged.connect(
            self.actualiser_solde
        )

        formulaire.addRow(
            "Élève :",
            self.select_eleve
        )

        # Montant
        self.champ_montant = QDoubleSpinBox()
        self.champ_montant.setMaximum(100000000)
        self.champ_montant.setDecimals(0)
        self.champ_montant.setSuffix(" FCFA")

        formulaire.addRow(
            "Montant payé :",
            self.champ_montant
        )

        # Date
        self.champ_date = QDateEdit()
        self.champ_date.setCalendarPopup(True)
        self.champ_date.setDate(
            self.champ_date.minimumDate().currentDate()
        )

        formulaire.addRow(
            "Date du paiement :",
            self.champ_date
        )

        # Mode de paiement
        self.select_mode = QComboBox()

        self.select_mode.addItems([
            "Espèces",
            "Chèque",
            "Virement",
            "Mobile Money"
        ])

        formulaire.addRow(
            "Mode de paiement :",
            self.select_mode
        )

        layout_carte.addLayout(formulaire)

        layout.addWidget(carte_formulaire)

        # Solde
        self.label_solde = QLabel(
            "Solde restant : 0 FCFA"
        )

        self.label_solde.setStyleSheet(
            f"font-size: 16px; font-weight: 700; color: {COULEUR_TEXTE_ATENUE};"
        )

        layout.addWidget(self.label_solde)

        # Bouton
        self.bouton_enregistrer = QPushButton(
            "Enregistrer le paiement"
        )
        self.bouton_enregistrer.setObjectName("primaire")

        self.bouton_enregistrer.clicked.connect(
            self.enregistrer_paiement
        )

        layout.addWidget(
            self.bouton_enregistrer
        )

        self.charger_eleves()

    def charger_eleves(self):
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

        self.actualiser_solde()

    def actualiser_solde(self):
        eleve_id = self.select_eleve.currentData()

        if eleve_id is None:
            self.label_solde.setText(
                "Solde restant : 0 FCFA"
            )
            return

        try:
            solde = self.paiement_service.calculer_solde(
                eleve_id
            )

            couleur = (
                COULEUR_SUCCES if solde <= 0 else COULEUR_TEXTE_ATENUE
            )

            self.label_solde.setStyleSheet(
                f"font-size: 16px; font-weight: 700; color: {couleur};"
            )

            self.label_solde.setText(
                f"Solde restant : {solde:,.0f} FCFA"
            )

        except ValueError as erreur:
            self.label_solde.setStyleSheet(
                f"font-size: 16px; font-weight: 700; color: {COULEUR_DANGER};"
            )

            self.label_solde.setText(
                f"Erreur : {erreur}"
            )

    def enregistrer_paiement(self):
        eleve_id = self.select_eleve.currentData()
        montant = self.champ_montant.value()

        if eleve_id is None:
            QMessageBox.warning(
                self,
                "Validation",
                "Veuillez sélectionner un élève."
            )
            return

        if montant <= 0:
            QMessageBox.warning(
                self,
                "Validation",
                "Le montant doit être supérieur à 0."
            )
            return

        date_paiement = (
            self.champ_date.date()
            .toString("yyyy-MM-dd")
        )

        mode_paiement = (
            self.select_mode.currentText()
        )

        numero_recu = self.generer_numero_recu()

        try:
            self.paiement_service.enregistrer_paiement(
                numero_recu,
                eleve_id,
                montant,
                date_paiement,
                mode_paiement
            )

            QMessageBox.information(
                self,
                "Succès",
                f"Paiement enregistré avec succès.\n\n"
                f"N° reçu : {numero_recu}"
            )

            self.champ_montant.setValue(0)

            self.actualiser_solde()

        except ValueError as erreur:
            QMessageBox.warning(
                self,
                "Paiement refusé",
                str(erreur)
            )

    def generer_numero_recu(self):
        annee = date.today().year

        return (
            self.paiement_service
            .paiement_repository
            .prochain_numero(annee)
        )