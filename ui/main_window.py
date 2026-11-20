import os
import sys
import webbrowser

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget
)

from ui.dashboard_page import DashboardPage
from ui.eleves_page import ElevesPage
from ui.paiements_page import PaiementsPage
from ui.historique_page import HistoriquePage
from ui.recus_page import RecusPage
from ui.parametres_page import ParametresPage
from ui.theme import COULEUR_SIDEBAR


class MainWindow(QMainWindow):
    def __init__(
        self,
        eleve_repository,
        paiement_service,
        dashboard_service,
        eleve_service,
        recu_service,
        parametres_service
    ):
        super().__init__()

        self.setWindowTitle(
            "EduPaie - Gestion des paiements scolaires"
        )

        self.resize(1200, 760)
        self.setMinimumSize(1000, 650)

        self.eleve_repository = eleve_repository
        self.paiement_service = paiement_service
        self.dashboard_service = dashboard_service
        self.eleve_service = eleve_service
        self.recu_service = recu_service
        self.parametres_service = parametres_service

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout_principal = QHBoxLayout(central_widget)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        # Barre latérale
        panneau = QFrame()
        panneau.setStyleSheet(
            f"background-color: {COULEUR_SIDEBAR};"
            "border-radius: 0px;"
        )
        panneau.setFixedWidth(200)

        layout_panneau = QVBoxLayout(panneau)
        layout_panneau.setContentsMargins(16, 24, 16, 24)
        layout_panneau.setSpacing(6)

        # Image de marque : logo + nom de l'établissement
        self.label_logo = QLabel()
        self.label_logo.setFixedSize(56, 56)
        self.label_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_nom_ecole = QLabel("EduPaie")
        self.label_nom_ecole.setStyleSheet(
            "font-size: 18px; font-weight: 700; color: #FFFFFF;"
        )
        self.label_nom_ecole.setWordWrap(True)

        self.label_sous_titre = QLabel("Paiements scolaires")
        self.label_sous_titre.setStyleSheet(
            "font-size: 11px; color: #94A3B8;"
        )

        layout_panneau.addWidget(self.label_logo)
        layout_panneau.addSpacing(6)
        layout_panneau.addWidget(self.label_nom_ecole)
        layout_panneau.addWidget(self.label_sous_titre)
        layout_panneau.addSpacing(22)

        # Pages
        self.pages = QStackedWidget()

        self.page_dashboard = DashboardPage(
            dashboard_service
        )

        self.page_eleves = ElevesPage(
            eleve_repository,
            eleve_service
        )

        self.page_paiements = PaiementsPage(
            eleve_repository,
            paiement_service
        )

        self.page_historique = HistoriquePage(
            eleve_repository,
            paiement_service.paiement_repository,
            paiement_service,
            recu_service,
            parametres_service
        )

        self.page_recus = RecusPage(
            eleve_repository,
            paiement_service.paiement_repository,
            paiement_service,
            parametres_service
        )

        self.page_parametres = ParametresPage(
            parametres_service,
            on_change=self.actualiser_image_de_marque
        )

        self.pages.addWidget(self.page_dashboard)
        self.pages.addWidget(self.page_eleves)
        self.pages.addWidget(self.page_paiements)
        self.pages.addWidget(self.page_historique)
        self.pages.addWidget(self.page_recus)
        self.pages.addWidget(self.page_parametres)

        # Navigation
        self.groupe_boutons = QButtonGroup(self)
        self.groupe_boutons.setExclusive(True)

        libelles_pages = [
            "Tableau de bord",
            "Élèves",
            "Paiements",
            "Historique",
            "Reçus",
            "Paramètres"
        ]

        for index, libelle in enumerate(libelles_pages):
            bouton = QPushButton(libelle)
            bouton.setObjectName("nav")
            bouton.setCheckable(True)
            bouton.setCursor(Qt.CursorShape.PointingHandCursor)

            bouton.clicked.connect(
                lambda checked=False, i=index:
                    self.pages.setCurrentIndex(i)
            )

            self.groupe_boutons.addButton(bouton, index)
            layout_panneau.addWidget(bouton)

        self.groupe_boutons.button(0).setChecked(True)

        layout_panneau.addStretch()

        # Liens d'aide en bas de la barre latérale
        self.bouton_confidentialite = QPushButton(
            "Politique de confidentialité"
        )
        self.bouton_confidentialite.setObjectName("lien")
        self.bouton_confidentialite.setCursor(
            Qt.CursorShape.PointingHandCursor
        )
        self.bouton_confidentialite.clicked.connect(
            lambda: self.ouvrir_document(
                "politique_confidentialite.html"
            )
        )

        self.bouton_documentation = QPushButton(
            "Documentation utilisateur"
        )
        self.bouton_documentation.setObjectName("lien")
        self.bouton_documentation.setCursor(
            Qt.CursorShape.PointingHandCursor
        )
        self.bouton_documentation.clicked.connect(
            lambda: self.ouvrir_document("documentation.html")
        )

        layout_panneau.addWidget(
            self.bouton_confidentialite
        )
        layout_panneau.addWidget(
            self.bouton_documentation
        )

        layout_principal.addWidget(panneau)

        # Zone de contenu
        zone_contenu = QWidget()
        layout_contenu = QVBoxLayout(zone_contenu)
        layout_contenu.setContentsMargins(24, 24, 24, 24)

        layout_contenu.addWidget(self.pages)

        layout_principal.addWidget(zone_contenu, 1)

        self.actualiser_image_de_marque()
        self.statusBar().showMessage("Prêt")

    def actualiser_image_de_marque(self):
        nom_ecole = self.parametres_service.nom_ecole()

        self.label_nom_ecole.setText(nom_ecole)
        self.setWindowTitle(
            f"{nom_ecole} - Paiements scolaires"
        )

        chemin_logo = self.parametres_service.chemin_logo()

        if chemin_logo and os.path.exists(chemin_logo):
            pixmap = QPixmap(chemin_logo)

            if not pixmap.isNull():
                self.label_logo.setPixmap(
                    pixmap.scaled(
                        48,
                        48,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                )
                return

        self.label_logo.setPixmap(QPixmap())
        self.label_logo.setText(nom_ecole[:1].upper())
        self.label_logo.setStyleSheet(
            "font-size: 22px; font-weight: 700; color: #FFFFFF;"
            f" background-color: {self.parametres_service.couleur_badge()};"
            " border-radius: 12px;"
        )

    @staticmethod
    def _chemin_document(nom_fichier):
        candidats = []

        if getattr(sys, "frozen", False):
            # Documentation intégrée à l'exécutable
            candidats.append(
                os.path.join(
                    getattr(sys, "_MEIPASS", ""),
                    "docs",
                    nom_fichier
                )
            )

            # Documentation placée à côté de l'exe
            candidats.append(
                os.path.join(
                    os.path.dirname(sys.executable),
                    "docs",
                    nom_fichier
                )
            )
        else:
            # Mode développement : dossier docs/ du projet
            candidats.append(
                os.path.join(
                    os.path.dirname(
                        os.path.dirname(
                            os.path.abspath(__file__)
                        )
                    ),
                    "docs",
                    nom_fichier
                )
            )

        for chemin in candidats:
            if chemin and os.path.exists(chemin):
                return chemin

        return None

    def ouvrir_document(self, nom_fichier):
        chemin = self._chemin_document(nom_fichier)

        if chemin is None:
            QMessageBox.information(
                self,
                "Document introuvable",
                "Le document demandé est introuvable."
            )
            return

        webbrowser.open(
            f"file:///{os.path.abspath(chemin)}"
        )
