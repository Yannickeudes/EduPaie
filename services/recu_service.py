import os

from reportlab.lib.colors import Color, HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


# Palette EduPaie
COULEUR_SUCCES = HexColor("#16A34A")
COULEUR_SUCCES_FOND = HexColor("#DCFCE7")
COULEUR_TEXTE = HexColor("#0F172A")
COULEUR_TEXTE_ATENUE = HexColor("#64748B")
COULEUR_BORDURE = HexColor("#E2E8F0")
COULEUR_BLANC = HexColor("#FFFFFF")

NOM_APPLICATION = "EduPaie"


def _couleur(valeur, facteur=1.0):
    valeur = valeur.lstrip("#")

    rouge = min(int(valeur[0:2], 16) / 255 * facteur, 1.0)
    vert = min(int(valeur[2:4], 16) / 255 * facteur, 1.0)
    bleu = min(int(valeur[4:6], 16) / 255 * facteur, 1.0)

    return Color(rouge, vert, bleu)


class RecuService:
    def generer_recu(
        self,
        numero_recu,
        eleve,
        montant,
        date_paiement,
        mode_paiement,
        solde_restant,
        nom_ecole=NOM_APPLICATION,
        chemin_logo=None,
        couleur_primaire="#2563EB"
    ):
        couleur = _couleur(couleur_primaire)
        couleur_fonce = _couleur(couleur_primaire, 0.8)
        os.makedirs("receipts", exist_ok=True)

        chemin = f"receipts/{numero_recu}.pdf"

        c = canvas.Canvas(chemin, pagesize=A4)

        largeur, hauteur = A4
        marge = 25 * mm
        largeur_disponible = largeur - 2 * marge

        # Bandeau supérieur
        hauteur_bandeau = 42 * mm
        c.setFillColor(couleur)
        c.rect(
            0,
            hauteur - hauteur_bandeau,
            largeur,
            hauteur_bandeau,
            stroke=0,
            fill=1
        )

        # Logo de l'établissement (si disponible)
        x_nom = largeur / 2
        largeur_logo = 0

        if chemin_logo and os.path.exists(chemin_logo):
            try:
                logo = ImageReader(chemin_logo)
                largeur_logo, hauteur_logo = logo.getSize()

                ratio = min(
                    30 * mm / largeur_logo,
                    30 * mm / hauteur_logo
                )

                largeur_affichee = largeur_logo * ratio
                hauteur_affichee = hauteur_logo * ratio

                c.drawImage(
                    logo,
                    marge,
                    hauteur - hauteur_bandeau
                    + (hauteur_bandeau - hauteur_affichee) / 2,
                    width=largeur_affichee,
                    height=hauteur_affichee,
                    mask="auto"
                )

                largeur_logo = largeur_affichee + 8 * mm
                x_nom = marge + largeur_affichee + 14 * mm
            except Exception:
                x_nom = largeur / 2
                largeur_logo = 0

        # Nom de l'établissement
        c.setFillColor(COULEUR_BLANC)

        if largeur_logo:
            c.setFont("Helvetica-Bold", 16)
            c.drawString(x_nom, hauteur - 19 * mm, nom_ecole)

            c.setFont("Helvetica", 9)
            c.drawString(
                x_nom,
                hauteur - 27 * mm,
                "Reçu de paiement scolaire"
            )
        else:
            c.setFont("Helvetica-Bold", 22)
            c.drawCentredString(
                largeur / 2,
                hauteur - 19 * mm,
                nom_ecole
            )

            c.setFont("Helvetica", 10)
            c.drawCentredString(
                largeur / 2,
                hauteur - 28 * mm,
                "Reçu de paiement scolaire"
            )

        # Titre du document
        y = hauteur - hauteur_bandeau - 18 * mm

        c.setFillColor(couleur_fonce)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(
            marge,
            y,
            "REÇU DE PAIEMENT"
        )

        # Badge PAYÉ
        largeur_badge = 32 * mm
        hauteur_badge = 10 * mm
        y_badge = y - 3 * mm

        c.setFillColor(COULEUR_SUCCES)
        c.roundRect(
            largeur - marge - largeur_badge,
            y_badge - hauteur_badge,
            largeur_badge,
            hauteur_badge,
            2 * mm,
            stroke=0,
            fill=1
        )

        c.setFillColor(COULEUR_BLANC)
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(
            largeur - marge - largeur_badge / 2,
            y_badge - hauteur_badge / 2 - 1.5 * mm,
            "PAYÉ"
        )

        # Ligne d'accentuation
        y -= 4 * mm
        c.setStrokeColor(couleur)
        c.setLineWidth(2)
        c.line(
            marge,
            y,
            marge + 30 * mm,
            y
        )

        # Numéro de reçu
        y -= 12 * mm
        c.setFillColor(COULEUR_TEXTE_ATENUE)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(
            marge,
            y,
            "N° REÇU"
        )

        c.setFillColor(COULEUR_TEXTE)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(
            marge + 28 * mm,
            y,
            numero_recu
        )

        # Cadre des informations
        y -= 10 * mm
        haut_cadre = y

        informations = [
            ("Élève", f"{eleve[1]} {eleve[2]}"),
            ("Classe", eleve[3]),
            ("Année scolaire", eleve[4]),
            ("Date du paiement", date_paiement),
            ("Mode de paiement", mode_paiement),
        ]

        for libelle, valeur in informations:
            c.setFillColor(COULEUR_TEXTE_ATENUE)
            c.setFont("Helvetica-Bold", 10)
            c.drawString(
                marge,
                y,
                libelle.upper()
            )

            c.setFillColor(COULEUR_TEXTE)
            c.setFont("Helvetica", 11)
            c.drawString(
                marge + 45 * mm,
                y,
                str(valeur)
            )

            y -= 9 * mm

        bas_cadre = y + 5 * mm

        c.setStrokeColor(COULEUR_BORDURE)
        c.setLineWidth(1)
        c.roundRect(
            marge,
            bas_cadre,
            largeur_disponible,
            haut_cadre - bas_cadre,
            3 * mm,
            stroke=1,
            fill=0
        )

        # Encadré du montant payé
        y = bas_cadre - 16 * mm
        hauteur_encadre = 22 * mm

        c.setFillColor(HexColor("#EFF6FF"))
        c.setStrokeColor(couleur)
        c.setLineWidth(1.5)
        c.roundRect(
            marge,
            y - hauteur_encadre + 8 * mm,
            largeur_disponible,
            hauteur_encadre,
            3 * mm,
            stroke=1,
            fill=1
        )

        c.setFillColor(couleur_fonce)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(
            marge + 6 * mm,
            y - 3 * mm,
            "MONTANT PAYÉ"
        )

        c.setFont("Helvetica-Bold", 16)
        c.drawRightString(
            marge + largeur_disponible - 6 * mm,
            y - 3 * mm,
            f"{montant:,.0f} FCFA"
        )

        c.setFillColor(COULEUR_TEXTE_ATENUE)
        c.setFont("Helvetica", 10)
        c.drawString(
            marge + 6 * mm,
            y - 11 * mm,
            f"Solde restant après paiement : "
            f"{solde_restant:,.0f} FCFA"
        )

        # Message de remerciement
        y_remerciement = 30 * mm

        c.setFillColor(COULEUR_SUCCES)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(
            largeur / 2,
            y_remerciement + 6 * mm,
            "Merci pour votre paiement."
        )

        c.setFillColor(COULEUR_TEXTE_ATENUE)
        c.setFont("Helvetica-Oblique", 9)
        c.drawCentredString(
            largeur / 2,
            y_remerciement,
            "Conservez ce reçu comme justificatif de paiement."
        )

        # Pied de page
        c.setStrokeColor(COULEUR_BORDURE)
        c.setLineWidth(1)
        c.line(
            marge,
            20 * mm,
            largeur - marge,
            20 * mm
        )

        c.setFillColor(COULEUR_TEXTE_ATENUE)
        c.setFont("Helvetica", 8)
        c.drawCentredString(
            largeur / 2,
            15 * mm,
            f"{nom_ecole} - Reçu généré automatiquement "
            f"par {NOM_APPLICATION}"
        )

        c.save()

        return chemin
