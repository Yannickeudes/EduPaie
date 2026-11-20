import os
import sys

from PySide6.QtWidgets import (
    QLabel,
    QTextBrowser,
    QTabWidget,
    QVBoxLayout,
    QWidget
)


def chemin_document(nom_fichier):
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


class AidePage(QWidget):
    DOCUMENTS = [
        (
            "documentation.html",
            "Documentation utilisateur"
        ),
        (
            "politique_confidentialite.html",
            "Politique de confidentialité"
        ),
    ]

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        titre = QLabel("Aide et documentation")
        titre.setObjectName("titre")

        layout.addWidget(titre)

        self.onglets = QTabWidget()

        for nom_fichier, libelle in self.DOCUMENTS:
            navigateur = QTextBrowser()
            navigateur.setOpenExternalLinks(True)
            navigateur.setStyleSheet(
                "QTextBrowser {"
                " background-color: #FFFFFF;"
                " border: 1px solid #E2E8F0;"
                " border-radius: 10px;"
                " padding: 14px;"
                "}"
            )

            chemin = chemin_document(nom_fichier)

            if chemin:
                with open(
                    chemin,
                    "r",
                    encoding="utf-8"
                ) as fichier:
                    navigateur.setHtml(fichier.read())
            else:
                navigateur.setHtml(
                    f"<h2>{libelle}</h2>"
                    "<p>Document introuvable.</p>"
                )

            self.onglets.addTab(navigateur, libelle)

        layout.addWidget(self.onglets)

    def afficher_nom(self, nom_fichier):
        for index, (fichier, _) in enumerate(self.DOCUMENTS):
            if fichier == nom_fichier:
                self.onglets.setCurrentIndex(index)
                return
