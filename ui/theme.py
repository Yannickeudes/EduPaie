from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem
)

# Palette EduPaie
COULEUR_PRIMAIRE = "#2563EB"
COULEUR_SUCCES = "#16A34A"
COULEUR_ATTENTION = "#D97706"
COULEUR_DANGER = "#DC2626"
COULEUR_SIDEBAR = "#0F172A"
COULEUR_FOND = "#F1F5F9"
COULEUR_CARTE = "#FFFFFF"
COULEUR_TEXTE = "#0F172A"
COULEUR_TEXTE_ATENUE = "#64748B"
COULEUR_BORDURE = "#E2E8F0"

COULEURS_STATUT = {
    "Soldé": COULEUR_SUCCES,
    "Partiellement payé": COULEUR_ATTENTION,
    "Non payé": COULEUR_DANGER,
}

_APPLICATION = None


def _vers_rgb(hexa):
    hexa = hexa.lstrip("#")
    return (
        int(hexa[0:2], 16),
        int(hexa[2:4], 16),
        int(hexa[4:6], 16),
    )


def _hex(rouge, vert, bleu):
    return "#{:02X}{:02X}{:02X}".format(
        max(0, min(255, int(rouge))),
        max(0, min(255, int(vert))),
        max(0, min(255, int(bleu))),
    )


def _fonce(hexa, facteur):
    r, v, b = _vers_rgb(hexa)
    return _hex(r * facteur, v * facteur, b * facteur)


def _clair(hexa, facteur):
    # Mélange avec le blanc : facteur = part de blanc (0 à 1)
    r, v, b = _vers_rgb(hexa)
    return _hex(
        r + (255 - r) * facteur,
        v + (255 - v) * facteur,
        b + (255 - b) * facteur,
    )


def stylesheet(couleur_primaire=COULEUR_PRIMAIRE):
    primaire = couleur_primaire
    primaire_fonce = _fonce(couleur_primaire, 0.85)
    primaire_fonce2 = _fonce(couleur_primaire, 0.7)
    primaire_clair = _clair(couleur_primaire, 0.93)
    selection = _clair(couleur_primaire, 0.88)
    bordure_claire = _clair(couleur_primaire, 0.78)
    accent_fonce = _fonce(couleur_primaire, 0.55)

    return f"""
QWidget {{
    background-color: {COULEUR_FOND};
    color: {COULEUR_TEXTE};
    font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    font-size: 13px;
}}

QMainWindow {{
    background-color: {COULEUR_FOND};
}}

/* Titres de pages */
QLabel#titre {{
    font-size: 22px;
    font-weight: 700;
    color: {COULEUR_TEXTE};
}}

QLabel#sous_titre {{
    font-size: 13px;
    color: {COULEUR_TEXTE_ATENUE};
}}

/* Cartes (indicateurs du tableau de bord) */
QFrame#carte {{
    background-color: {COULEUR_CARTE};
    border: 1px solid {COULEUR_BORDURE};
    border-radius: 12px;
}}

/* Boutons */
QPushButton {{
    background-color: #E2E8F0;
    color: {COULEUR_TEXTE};
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    padding: 8px 16px;
}}

QPushButton:hover {{
    background-color: #CBD5E1;
}}

QPushButton:pressed {{
    background-color: #94A3B8;
}}

QPushButton:disabled {{
    background-color: {COULEUR_FOND};
    color: #94A3B8;
    border-color: {COULEUR_BORDURE};
}}

QPushButton#primaire {{
    background-color: {primaire};
    color: #FFFFFF;
    border: none;
    font-weight: 600;
}}

QPushButton#primaire:hover {{
    background-color: {primaire_fonce};
}}

QPushButton#primaire:pressed {{
    background-color: {primaire_fonce2};
}}

QPushButton#secondaire {{
    background-color: #FFFFFF;
    color: {primaire};
    border: 1px solid {primaire};
}}

QPushButton#secondaire:hover {{
    background-color: {primaire_clair};
}}

QPushButton#danger {{
    background-color: {COULEUR_DANGER};
    color: #FFFFFF;
    border: none;
    font-weight: 600;
}}

QPushButton#danger:hover {{
    background-color: #B91C1C;
}}

/* Boutons de navigation (barre latérale) */
QPushButton#nav {{
    background-color: transparent;
    color: #CBD5E1;
    border: none;
    border-radius: 8px;
    padding: 11px 14px;
    text-align: left;
    font-size: 14px;
}}

QPushButton#nav:hover {{
    background-color: #1E293B;
    color: #FFFFFF;
}}

/* Liens d'aide en bas de la barre latérale */
QPushButton#lien {{
    background-color: transparent;
    color: #94A3B8;
    border: none;
    border-radius: 6px;
    padding: 6px 10px;
    text-align: left;
    font-size: 12px;
}}

QPushButton#lien:hover {{
    background-color: #1E293B;
    color: #FFFFFF;
}}

QPushButton#nav:checked {{
    background-color: {primaire};
    color: #FFFFFF;
    font-weight: 600;
}}

/* Champs de saisie */
QLineEdit,
QComboBox,
QDoubleSpinBox,
QDateEdit {{
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    padding: 6px 10px;
    selection-background-color: {selection};
}}

QLineEdit:focus,
QComboBox:focus,
QDoubleSpinBox:focus,
QDateEdit:focus {{
    border: 1px solid {primaire};
}}

QComboBox QAbstractItemView {{
    background-color: #FFFFFF;
    border: 1px solid {COULEUR_BORDURE};
    selection-background-color: {selection};
    selection-color: {COULEUR_TEXTE};
    outline: none;
}}

QComboBox::drop-down {{
    border: none;
    width: 24px;
}}

/* Formulaires */
QFormLayout QLabel {{
    color: {COULEUR_TEXTE_ATENUE};
}}

/* Tableaux */
QTableWidget {{
    background-color: #FFFFFF;
    alternate-background-color: #F8FAFC;
    border: 1px solid {COULEUR_BORDURE};
    border-radius: 10px;
    gridline-color: #EEF2F7;
    selection-background-color: {selection};
    selection-color: {COULEUR_TEXTE};
}}

QTableWidget::item {{
    padding: 6px;
}}

QTableWidget::item:alternate {{
    background-color: #F8FAFC;
}}

QHeaderView::section {{
    background-color: {primaire_clair};
    color: {accent_fonce};
    font-weight: 600;
    padding: 8px;
    border: none;
    border-bottom: 2px solid {bordure_claire};
}}

/* Onglets (page Aide) */
QTabWidget::pane {{
    border: 1px solid {COULEUR_BORDURE};
    border-radius: 10px;
    top: -1px;
    background-color: #FFFFFF;
}}

QTabBar::tab {{
    background-color: #E2E8F0;
    color: #334155;
    padding: 8px 20px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    margin-right: 4px;
}}

QTabBar::tab:selected {{
    background-color: {primaire};
    color: #FFFFFF;
    font-weight: 600;
}}

QTabBar::tab:hover:!selected {{
    background-color: #CBD5E1;
}}

/* Barres de défilement */
QScrollBar:vertical {{
    background: transparent;
    width: 10px;
    margin: 0;
}}

QScrollBar::handle:vertical {{
    background: #CBD5E1;
    border-radius: 5px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background: #94A3B8;
}}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {{
    height: 0;
}}

QScrollBar:horizontal {{
    background: transparent;
    height: 10px;
    margin: 0;
}}

QScrollBar::handle:horizontal {{
    background: #CBD5E1;
    border-radius: 5px;
    min-width: 30px;
}}

QScrollBar::handle:horizontal:hover {{
    background: #94A3B8;
}}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {{
    width: 0;
}}

/* Barre d'état */
QStatusBar {{
    background-color: #FFFFFF;
    color: {COULEUR_TEXTE_ATENUE};
    border-top: 1px solid {COULEUR_BORDURE};
}}
"""


def appliquer_theme(application, couleur_primaire=None):
    global _APPLICATION

    _APPLICATION = application

    application.setStyle("Fusion")
    application.setStyleSheet(
        stylesheet(couleur_primaire or COULEUR_PRIMAIRE)
    )


def actualiser_couleur(couleur_primaire):
    if _APPLICATION is not None:
        _APPLICATION.setStyleSheet(
            stylesheet(couleur_primaire)
        )


def configurer_tableau(tableau: QTableWidget):
    tableau.setAlternatingRowColors(True)
    tableau.setSelectionBehavior(
        QAbstractItemView.SelectionBehavior.SelectRows
    )
    tableau.setSelectionMode(
        QAbstractItemView.SelectionMode.SingleSelection
    )
    tableau.verticalHeader().setVisible(False)
    tableau.horizontalHeader().setSectionResizeMode(
        QHeaderView.ResizeMode.Interactive
    )
    tableau.horizontalHeader().setStretchLastSection(True)


def item_colore(texte, couleur, gras=False):
    item = QTableWidgetItem(str(texte))
    item.setForeground(QColor(couleur))

    if gras:
        police = item.font()
        police.setBold(True)
        item.setFont(police)

    return item


def couleur_statut(statut):
    return COULEURS_STATUT.get(statut, COULEUR_TEXTE)


def item_statut(statut):
    return item_colore(statut, couleur_statut(statut), gras=True)
