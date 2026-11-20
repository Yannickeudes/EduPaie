from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
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
from ui.theme import COULEUR_SIDEBAR


class MainWindow(QMainWindow):
    def __init__(
        self,
        eleve_repository,
        paiement_service,
        dashboard_service,
        eleve_service,
        recu_service
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

        titre = QLabel("EduPaie")
        titre.setStyleSheet(
            "font-size: 26px; font-weight: 700; color: #FFFFFF;"
        )

        sous_titre = QLabel("Paiements scolaires")
        sous_titre.setStyleSheet(
            "font-size: 12px; color: #94A3B8;"
        )

        layout_panneau.addWidget(titre)
        layout_panneau.addWidget(sous_titre)
        layout_panneau.addSpacing(28)

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
            recu_service
        )

        self.page_recus = RecusPage(
            eleve_repository,
            paiement_service.paiement_repository,
            paiement_service
        )

        self.pages.addWidget(self.page_dashboard)
        self.pages.addWidget(self.page_eleves)
        self.pages.addWidget(self.page_paiements)
        self.pages.addWidget(self.page_historique)
        self.pages.addWidget(self.page_recus)

        # Navigation
        self.groupe_boutons = QButtonGroup(self)
        self.groupe_boutons.setExclusive(True)

        libelles_pages = [
            "Tableau de bord",
            "Élèves",
            "Paiements",
            "Historique",
            "Reçus"
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

        layout_principal.addWidget(panneau)

        # Zone de contenu
        zone_contenu = QWidget()
        layout_contenu = QVBoxLayout(zone_contenu)
        layout_contenu.setContentsMargins(24, 24, 24, 24)

        layout_contenu.addWidget(self.pages)

        layout_principal.addWidget(zone_contenu, 1)

        self.statusBar().showMessage("Prêt")
