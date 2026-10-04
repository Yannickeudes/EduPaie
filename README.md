# EduPaie

EduPaie est une application desktop de gestion des paiements scolaires.

Elle permet de gérer les élèves, enregistrer les paiements, suivre les soldes, consulter l'historique des paiements, générer des reçus PDF et consulter un tableau de bord.

## Fonctionnalités

- Ajouter, modifier et supprimer un élève
- Rechercher un élève
- Filtrer les élèves par classe
- Enregistrer un paiement
- Gérer plusieurs paiements pour un même élève
- Calculer automatiquement le montant payé et le solde restant
- Déterminer le statut d'un élève :
  - Non payé
  - Partiellement payé
  - Soldé
- Consulter l'historique des paiements
- Générer et réouvrir les reçus PDF
- Consulter les statistiques du tableau de bord
- Afficher les données de démonstration

## Technologies utilisées

- Python 3.10+
- PySide6
- SQLite
- ReportLab
- unittest

## Architecture

Le projet suit une séparation en trois couches principales :

```text
UI
 ↓
Services
 ↓
Repositories
 ↓
SQLite