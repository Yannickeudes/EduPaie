import sys
from database.database import initialiser_base

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QDialog

from repositories.eleve_repository import EleveRepository
from repositories.paiement_repository import PaiementRepository
from repositories.parametre_repository import ParametreRepository
from repositories.utilisateur_repository import UtilisateurRepository

from services.paiement_service import PaiementService
from services.eleve_service import EleveService
from services.recu_service import RecuService
from services.dashboard_service import DashboardService
from services.parametres_service import ParametresService
from services.auth_service import AuthService

from ui.auth_dialogs import (
    ConfigurationComptesDialog,
    LoginDialog
)

from ui.main_window import MainWindow
from ui.theme import appliquer_theme


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

parametre_repository = ParametreRepository(connection)

parametres_service = ParametresService(
    parametre_repository
)

utilisateur_repository = UtilisateurRepository(
    connection
)

auth_service = AuthService(
    utilisateur_repository
)

app = QApplication(sys.argv)
appliquer_theme(
    app,
    parametres_service.couleur_badge()
)

# La fenêtre peut être fermée sans quitter
# l'application (déconnexion puis reconnexion)
app.setQuitOnLastWindowClosed(False)


def proposer_connexion():
    # Premier lancement : configuration des mots de passe
    if not auth_service.comptes_configures():
        configuration = ConfigurationComptesDialog(
            auth_service
        )

        if (
            configuration.exec()
            != QDialog.DialogCode.Accepted
        ):
            app.quit()
            return

    # Connexion
    connexion = LoginDialog(auth_service)

    if (
        connexion.exec()
        != QDialog.DialogCode.Accepted
    ):
        app.quit()
        return

    ouvrir_fenetre(connexion.utilisateur)


def ouvrir_fenetre(utilisateur):
    fenetre = MainWindow(
        eleve_repository,
        paiement_service,
        dashboard_service,
        eleve_service,
        recu_service,
        parametres_service,
        auth_service,
        utilisateur
    )

    fenetre.deconnexion_demandee.connect(
        lambda: fermer_et_reconnecter(fenetre)
    )

    fenetre.show()


def fermer_et_reconnecter(fenetre):
    fenetre.close()
    fenetre.deleteLater()

    proposer_connexion()


QTimer.singleShot(0, proposer_connexion)

exit_code = app.exec()

connection.close()

sys.exit(exit_code)