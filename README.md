# VeriDIC - La donnée, à portée de clic.

## Vue d'ensemble
VeriDIC est conçu pour automatiser le processus d'extraction de données des Documents d'Information Clef (DIC) ainsi que leur analyse. Ce système utilise GPT4 pour interpréter intelligemment les documents financiers et les convertir en données structurées faciles à analyser et à traiter. Le système comprend également une application web construite avec Streamlit pour faciliter l'interaction des utilisateurs et la navigation dans les données.

## Architecture du système

### Entrée
- **DIC au format PDF** : Le système accepte les DICs en format PDF comme entrée.

### Traitement
- **Python** : Le traitement principal est réalisé en utilisant Python, impliquant les éléments suivants :
  - Extraction de texte à partir de PDFs.
  - Utilisation des LLMs pour comprendre et structurer les données.
  - Réalisation d'analyses de similarité sémantique sur les descriptions de produits pour créer des sorties structurées.
  - Détection d'anomalies et génération d'aperçus.

### Sortie
- **CSV avec caractéristiques** : Les données structurées sont produites sous forme de fichier CSV avec des caractéristiques adaptées pour des analyses ou visualisations ultérieures.
- **Application Web (Streamlit)** : Une application web basée sur Streamlit qui offre une interface interactive pour les utilisateurs afin de naviguer dans les données de sortie.

## Fonctionnalités

- **Extraction de données** : Méthodes d'extraction robustes pour gérer différents formats et styles de documents.
- **Analyse sémantique** : LLMs utilisés pour apporter un contexte et une compréhension sémantique aux données structurées.
- **Détection d'anomalies** : Le système inclut une fonctionnalité de détection d'anomalies pour identifier les points de données qui s'écartent des modèles attendus.
- **Interface utilisateur** : Une application web conviviale pour la visualisation et la navigation des données.
- **Scalabilité** : Conçu pour répondre aux besoins de scalabilité, rendant le système adapté au traitement d'un grand volume de documents.
- **Sensibilité ajustable** : Paramètres de sensibilité ajustables pour la tolérance de l'invite du LLM afin d'affiner la complexité de l'analyse.

## Points forts

- **Score de similarité** : Utilisation du clustering pour déterminer la similarité entre différents produits financiers.
- **Score de compréhensibilité** : Évaluation de la facilité de compréhension des données par les utilisateurs finaux.
- **Graphe de produits structurés** : Représentation visuelle des relations entre les produits structurés.
- **Facilité d'utilisation** : Scalabilité et interface conviviale pour une expérience utilisateur sans heurt.
- **Base de données explorables** : La base de données de sortie (BDD) peut être explorée sans surcharger le système.

## Utilisation

1. **Entrée de données** : Téléversez vos PDFs de DIC dans le système.
2. **Traitement des données** : Exécutez les scripts Python pour traiter les documents via les LLMs.
3. **Examen de la sortie** : Examinez le fichier CSV de sortie et utilisez l'application web Streamlit pour l'exploration interactive des données.
4. **Analyse des données** : Utilisez les scores de similarité et de compréhensibilité pour analyser les données structurées.
5. **Détection d'anomalies** : Appliquez la fonctionnalité de détection d'anomalies pour préserver l'intégrité de vos données.

## Installation
