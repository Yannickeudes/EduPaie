import os
import re
import shutil
import time

from database.database import obtenir_chemin_base

NOM_DEFAUT = "EduPaie"
CLE_NOM_ECOLE = "nom_ecole"
CLE_LOGO = "logo"
CLE_COULEUR_BADGE = "couleur_badge"
COULEUR_DEFAUT = "#2563EB"


class ParametresService:
    def __init__(self, parametre_repository):
        self.parametre_repository = parametre_repository

    def nom_ecole(self):
        return self.parametre_repository.obtenir(
            CLE_NOM_ECOLE,
            NOM_DEFAUT
        )

    def couleur_badge(self):
        return self.parametre_repository.obtenir(
            CLE_COULEUR_BADGE,
            COULEUR_DEFAUT
        )

    def nom_fichier_logo(self):
        return self.parametre_repository.obtenir(
            CLE_LOGO,
            ""
        )

    def dossier_logos(self):
        dossier_base = os.path.dirname(
            obtenir_chemin_base()
        )

        return os.path.join(
            dossier_base,
            "logos"
        )

    def chemin_logo(self):
        nom_fichier = self.nom_fichier_logo()

        if not nom_fichier:
            return None

        chemin = os.path.join(
            self.dossier_logos(),
            nom_fichier
        )

        if os.path.exists(chemin):
            return chemin

        return None

    def enregistrer(
        self,
        nom_ecole,
        chemin_logo_source=None,
        couleur=None
    ):
        nom_ecole = nom_ecole.strip()

        if not nom_ecole:
            raise ValueError(
                "Le nom de l'établissement est obligatoire."
            )

        self.parametre_repository.definir(
            CLE_NOM_ECOLE,
            nom_ecole
        )

        if couleur:
            couleur = couleur.strip()

            if not re.fullmatch(
                r"#[0-9A-Fa-f]{6}", couleur
            ):
                raise ValueError(
                    "Couleur invalide "
                    "(format #RRGGBB attendu)."
                )

            self.parametre_repository.definir(
                CLE_COULEUR_BADGE,
                couleur.upper()
            )

        if chemin_logo_source:
            nom_fichier_logo = self._copier_logo(
                chemin_logo_source
            )

            self.parametre_repository.definir(
                CLE_LOGO,
                nom_fichier_logo
            )

    def supprimer_logo(self):
        self.parametre_repository.definir(
            CLE_LOGO,
            ""
        )

    def _copier_logo(self, chemin_source):
        if not os.path.exists(chemin_source):
            raise ValueError(
                "Le fichier logo est introuvable."
            )

        extension = os.path.splitext(
            chemin_source
        )[1].lower()

        extensions_valables = (
            ".png",
            ".jpg",
            ".jpeg",
            ".bmp",
            ".gif",
            ".ico",
            ".webp"
        )

        if extension not in extensions_valables:
            raise ValueError(
                "Format de logo non pris en charge. "
                "Utilisez PNG, JPG, BMP, GIF, ICO ou WebP."
            )

        dossier = self.dossier_logos()

        os.makedirs(dossier, exist_ok=True)

        nom_fichier = (
            f"logo_{int(time.time())}{extension}"
        )

        destination = os.path.join(
            dossier,
            nom_fichier
        )

        shutil.copy2(
            chemin_source,
            destination
        )

        return nom_fichier
