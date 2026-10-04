import sys
from database.database import initialiser_base

from PySide6.QtWidgets import QApplication

from repositories.eleve_repository import EleveRepository
from repositories.paiement_repository import PaiementRepository

from services.paiement_service import PaiementService
from services.eleve_service import EleveService
from services.recu_service import RecuService
from services.dashboard_service import DashboardService

from ui.main_window import MainWindow


connection = initialiser_base()

eleve_repository = EleveRepository(connection)
paiement_repository = PaiementRepository(connection)

paiement_service = PaiementService(
    eleve_repository,
    paiement_repository
)

eleve_service = EleveService(
    eleve_repository,
    paiement_service
)

recu_service = RecuService()

dashboard_service = DashboardService(
    eleve_repository,
    paiement_service
)

app = QApplication(sys.argv)

window = MainWindow(
    eleve_repository,
    paiement_service,
    dashboard_service,
    eleve_service,
    recu_service
)

window.show()

exit_code = app.exec()

connection.close()

sys.exit(exit_code)