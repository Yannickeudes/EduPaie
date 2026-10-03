
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import os


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

        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(
            largeur / 2,
            hauteur - 30 * mm,
            "EDUPAIE"
        )

        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(
            largeur / 2,
            hauteur - 45 * mm,
            "REÇU DE PAIEMENT"
        )

        y = hauteur - 70 * mm

        c.setFont("Helvetica", 11)

        c.drawString(
            30 * mm,
            y,
            f"N° reçu : {numero_recu}"
        )
        y -= 10 * mm

        c.drawString(
            30 * mm,
            y,
            f"Nom : {eleve[1]}"
        )
        y -= 8 * mm

        c.drawString(
            30 * mm,
            y,
            f"Prénom : {eleve[2]}"
        )
        y -= 8 * mm

        c.drawString(
            30 * mm,
            y,
            f"Classe : {eleve[3]}"
        )
        y -= 8 * mm

        c.drawString(
            30 * mm,
            y,
            f"Année scolaire : {eleve[4]}"
        )
        y -= 15 * mm

        c.drawString(
            30 * mm,
            y,
            f"Montant payé : {montant:,.0f} FCFA"
        )
        y -= 8 * mm

        c.drawString(
            30 * mm,
            y,
            f"Date : {date_paiement}"
        )
        y -= 8 * mm

        c.drawString(
            30 * mm,
            y,
            f"Mode de paiement : {mode_paiement}"
        )
        y -= 8 * mm

        c.drawString(
            30 * mm,
            y,
            f"Solde restant : {solde_restant:,.0f} FCFA"
        )

        y -= 25 * mm

        c.setFont("Helvetica-Oblique", 10)
        c.drawString(
            30 * mm,
            y,
            "Merci pour votre paiement."
        )

        c.save()

        return chemin
