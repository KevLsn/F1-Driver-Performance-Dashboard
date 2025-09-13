## F1 Driver Performance Dashboard

### Description
Le F1 Driver Performance Dashboard est un outil Python interactif permetant de comparer les performances des pilotes de Formule 1 sur une session. Le projet utilise FastF1 pour récupérer les données officielles des sessions (qualifications, courses et essais) et fournit des visualisations détaillées de la télémétrie des pilotes.

Avec ce dashboard, tu peux :
Choisir l’année, le Grand Prix et le type de session.
Comparer le meilleur tour de deux pilotes.
Visualiser la vitesse en fonction de la distance parcourue.

Ce projet peut être la base d’un dashboard interactif pour visualiser la performance F1, ou être étendu pour analyser plusieurs courses et saisons.

### Fonctionnalités principales
Sélection interactive de la session F1 et des pilotes.
Récupération automatique des données via FastF1 et mise en cache locale.
Visualisation des meilleurs tours des pilotes.
Comparaison graphique des vitesses.
Gestion des erreurs pour les saisies invalides ou les pilotes absents.

### Technologies utilisées
Python 3.9+
FastF1 : récupération et traitement des données F1.
Matplotlib : visualisation graphique des vitesses et secteurs.
Pandas : manipulation des données télémétriques.