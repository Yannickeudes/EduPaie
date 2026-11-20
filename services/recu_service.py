import os

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


# Palette EduPaie
COULEUR_PRIMAIRE = HexColor("#2563EB")
COULEUR_PRIMAIRE_FONCE = HexColor("#1D4ED8")
COULEUR_SUCCES = HexColor("#16A34A")
COULEUR_TEXTE = HexColor("#0F172A")
COULEUR_TEXTE_ATENUE = HexColor("#64748B")
COULEUR_BORDURE = HexColor("#E2E8F0")
COULEUR_FOND_LIGNE = HexColor("#F1F5F9")


class RecuService:
    def generer_recu(
        self,
        numero_recu,
        eleve,
        montant,
        date_paiement,
        mode_paiement,
        solde_restant
    ):
        os.makedirs("receipts", exist_ok=True)

        chemin = f"receipts/{numero_recu}.pdf"

        c = canvas.Canvas(chemin, pagesize=A4)

        largeur, hauteur = A4
        marge = 25 * mm
        largeur_disponible = largeur - 2 * marge

        # Bandeau supérieur
        hauteur_bandeau = 42 * mm
        c.setFillColor(COULEUR_PRIMAIRE)
        c.rect(
            0,
            hauteur - hauteur_bandeau,
            largeur,
            hauteur_bandeau,
            stroke=0,
            fill=1
        )

        c.setFillColor(HexColor("#FFFFFF"))

        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(
            largeur / 2,
            hauteur - 20 * mm,
            "EDUPAIE"
        )

        c.setFont("Helvetica", 10)
        c.drawCentredString(
            largeur / 2,
            hauteur - 29 * mm,
            "Gestion des paiements scolaires"
        )

        # Titre du document
        y = hauteur - hauteur_bandeau - 18 * mm

        c.setFillColor(COULEUR_PRIMAIRE_FONCE)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(
            marge,
            y,
            "REÇU DE PAIEMENT"
        )

        # Ligne d'accentuation
        y -= 4 * mm
        c.setStrokeColor(COULEUR_PRIMAIRE)
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
        c.setStrokeColor(COULEUR_PRIMAIRE)
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

        c.setFillColor(COULEUR_PRIMAIRE_FONCE)
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
            "EduPaie - Reçu généré automatiquement"
        )

        c.save()

        return chemin
