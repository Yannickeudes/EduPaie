from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget
)

from ui.dashboard_page import DashboardPage
from ui.eleves_page import ElevesPage
from ui.paiements_page import PaiementsPage
from ui.historique_page import HistoriquePage
from ui.recus_page import RecusPage


class MainWindow(QMainWindow):
    def __init__(
        self,
        eleve_repository,
        paiement_service,
        dashboard_service
    ):
        super().__init__()

        self.setWindowTitle(
            "EduPaie - Gestion des paiements scolaires"
        )

        self.resize(1000, 650)

        central_widget = QWidget()

        self.setCentralWidget(
            central_widget
        )

        layout_principal = QVBoxLayout(
            central_widget
        )

        # Titre
        titre = QLabel("EduPaie")

        titre.setStyleSheet(
            "font-size: 28px; font-weight: bold;"
        )

        layout_principal.addWidget(
            titre
        )

        # Navigation
        self.bouton_dashboard = QPushButton(
            "Tableau de bord"
        )

        self.bouton_eleves = QPushButton(
            "Élèves"
        )

        self.bouton_paiements = QPushButton(
            "Paiements"
        )

        self.bouton_historique = QPushButton(
            "Historique"
        )

        self.bouton_recus = QPushButton(
            "Reçus"
        )

        layout_principal.addWidget(
            self.bouton_dashboard
        )

        layout_principal.addWidget(
            self.bouton_eleves
        )

        layout_principal.addWidget(
            self.bouton_paiements
        )

        layout_principal.addWidget(
            self.bouton_historique
        )

        layout_principal.addWidget(
            self.bouton_recus
        )

        # Pages
        self.pages = QStackedWidget()

        self.page_dashboard = DashboardPage(
            dashboard_service
        )

        self.page_eleves = ElevesPage(
            eleve_repository
        )

        self.page_paiements = PaiementsPage(
            eleve_repository,
            paiement_service
        )

        self.page_historique = HistoriquePage(
            eleve_repository,
            paiement_service.paiement_repository,
            paiement_service
        )

        self.page_recus = RecusPage(
            eleve_repository,
            paiement_service.paiement_repository,
            paiement_service
        )

        # Ajout des pages
        self.pages.addWidget(
            self.page_dashboard
        )

        self.pages.addWidget(
            self.page_eleves
        )

        self.pages.addWidget(
            self.page_paiements
        )

        self.pages.addWidget(
            self.page_historique
        )

        self.pages.addWidget(
            self.page_recus
        )

        layout_principal.addWidget(
            self.pages
        )

        # Navigation
        self.bouton_dashboard.clicked.connect(
            lambda: self.pages.setCurrentIndex(0)
        )

        self.bouton_eleves.clicked.connect(
            lambda: self.pages.setCurrentIndex(1)
        )

        self.bouton_paiements.clicked.connect(
            lambda: self.pages.setCurrentIndex(2)
        )

        self.bouton_historique.clicked.connect(
            lambda: self.pages.setCurrentIndex(3)
        )

        self.bouton_recus.clicked.connect(
            lambda: self.pages.setCurrentIndex(4)
        )
