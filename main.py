
import sys
import sqlite3

from PySide6.QtWidgets import QApplication

from repositories.eleve_repository import EleveRepository
from repositories.paiement_repository import PaiementRepository

from services.paiement_service import PaiementService
from services.eleve_service import EleveService
from services.dashboard_service import DashboardService

from ui.main_window import MainWindow


# Connexion à la base de données
connection = sqlite3.connect(
    "database/edupaie.db"
)

# Repositories
eleve_repository = EleveRepository(
    connection
)

paiement_repository = PaiementRepository(
    connection
)

# Service des paiements
paiement_service = PaiementService(
    eleve_repository,
    paiement_repository
)

# Service des élèves
eleve_service = EleveService(
    eleve_repository,
    paiement_service
)

# Service du tableau de bord
dashboard_service = DashboardService(
    eleve_repository,
    paiement_service
)

# Application
app = QApplication(
    sys.argv
)

# Fenêtre principale
window = MainWindow(
    eleve_repository,
    paiement_service,
    dashboard_service,
    eleve_service
)

window.show()

exit_code = app.exec()

connection.close()

sys.exit(exit_code)
