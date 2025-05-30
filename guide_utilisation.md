# Guide d'installation et d'utilisation

Ce document fournit des instructions détaillées pour l'installation, la configuration et l'utilisation de l'application d'analyse boursière.

## Table des matières

1. [Installation](#installation)
   - [Prérequis](#prérequis)
   - [Installation avec Docker](#installation-avec-docker)
   - [Installation manuelle](#installation-manuelle)
2. [Configuration](#configuration)
   - [Variables d'environnement](#variables-denvironnement)
   - [Configuration des API financières](#configuration-des-api-financières)
   - [Configuration des notifications](#configuration-des-notifications)
3. [Utilisation](#utilisation)
   - [Tableau de bord](#tableau-de-bord)
   - [Analyse technique](#analyse-technique)
   - [Concepts ICT](#concepts-ict)
   - [Gestion de portefeuille](#gestion-de-portefeuille)
   - [Alertes](#alertes)
4. [Dépannage](#dépannage)
   - [Problèmes courants](#problèmes-courants)
   - [Logs](#logs)

## Installation

### Prérequis

- Docker et Docker Compose (recommandé)
- Ou Python 3.9+ et Node.js 16+ pour l'installation manuelle
- Un serveur VPS ou une machine avec au moins 2 Go de RAM
- Accès à Internet pour les API financières

### Installation avec Docker

1. Clonez le dépôt GitHub :
   ```bash
   git clone https://github.com/votre-username/finance-app.git
   cd finance-app
   ```

2. Créez un fichier `.env` à la racine du projet avec les variables d'environnement nécessaires (voir section Configuration).

3. Lancez l'application avec Docker Compose :
   ```bash
   docker-compose up -d
   ```

4. Vérifiez que tous les services sont en cours d'exécution :
   ```bash
   docker-compose ps
   ```

5. Accédez à l'application via votre navigateur à l'adresse `http://localhost` ou à l'adresse IP de votre serveur.

### Installation manuelle

#### Backend

1. Accédez au répertoire backend :
   ```bash
   cd finance-app/backend
   ```

2. Créez et activez un environnement virtuel Python :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows : venv\Scripts\activate
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. Configurez les variables d'environnement (voir section Configuration).

5. Lancez le serveur :
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

#### Frontend

1. Accédez au répertoire frontend :
   ```bash
   cd finance-app/frontend
   ```

2. Installez les dépendances :
   ```bash
   npm install
   ```

3. Construisez l'application pour la production :
   ```bash
   npm run build
   ```

4. Servez l'application avec un serveur HTTP :
   ```bash
   npm install -g serve
   serve -s dist -l 80
   ```

#### Base de données

1. Installez PostgreSQL et Redis selon les instructions de votre système d'exploitation.

2. Créez une base de données pour l'application :
   ```bash
   createdb finance_app
   ```

3. Configurez les variables d'environnement pour la connexion à la base de données.

## Configuration

### Variables d'environnement

Créez un fichier `.env` à la racine du projet avec les variables suivantes :

```
# Base de données
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=finance_app

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Sécurité
SECRET_KEY=votre-clé-secrète-pour-jwt

# API financières
ALPHAVANTAGE_API_KEY=votre-clé-api-alphavantage
FINNHUB_API_KEY=votre-clé-api-finnhub

# Notifications
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=votre-email@gmail.com
EMAIL_PASSWORD=votre-mot-de-passe-email
TELEGRAM_BOT_TOKEN=votre-token-telegram-bot
```

### Configuration des API financières

L'application utilise par défaut l'API Yahoo Finance qui ne nécessite pas de clé API. Cependant, pour des fonctionnalités avancées ou une utilisation intensive, vous pouvez configurer d'autres API :

#### Alpha Vantage
1. Créez un compte sur [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
2. Obtenez une clé API gratuite
3. Ajoutez la clé à la variable d'environnement `ALPHAVANTAGE_API_KEY`

#### Finnhub
1. Créez un compte sur [Finnhub](https://finnhub.io/register)
2. Obtenez une clé API
3. Ajoutez la clé à la variable d'environnement `FINNHUB_API_KEY`

### Configuration des notifications

#### Email
1. Configurez les variables d'environnement `EMAIL_*`
2. Pour Gmail, vous devrez peut-être activer l'accès des applications moins sécurisées ou utiliser un mot de passe d'application

#### Telegram
1. Créez un bot Telegram via [@BotFather](https://t.me/botfather)
2. Obtenez le token du bot et configurez-le dans la variable d'environnement `TELEGRAM_BOT_TOKEN`
3. Démarrez une conversation avec votre bot
4. Pour obtenir votre ID de chat, utilisez le bot [@userinfobot](https://t.me/userinfobot)
5. Dans l'application, activez les notifications Telegram et entrez votre ID de chat

#### WhatsApp
L'intégration WhatsApp nécessite un compte WhatsApp Business API. Pour une configuration complète :
1. Créez un compte sur [WhatsApp Business Platform](https://developers.facebook.com/docs/whatsapp/getting-started)
2. Suivez les instructions pour obtenir un accès à l'API
3. Configurez les paramètres dans l'interface utilisateur de l'application

## Utilisation

### Tableau de bord

Le tableau de bord est la page d'accueil de l'application. Il présente une vue d'ensemble personnalisable de vos actifs, indicateurs et alertes.

#### Personnalisation du tableau de bord
1. Cliquez sur le bouton "Modifier" en haut à droite
2. Ajoutez, supprimez ou réorganisez les widgets selon vos préférences
3. Cliquez sur "Enregistrer" pour sauvegarder votre configuration

### Analyse technique

L'écran d'analyse technique vous permet d'étudier en détail les actifs financiers.

#### Recherche d'actifs
1. Utilisez la barre de recherche en haut de l'écran
2. Entrez le symbole ou le nom de l'actif (ex: AAPL, BTC-USD, EUR=)
3. Sélectionnez l'actif dans les résultats de recherche

#### Ajout d'indicateurs techniques
1. Cliquez sur le bouton "Indicateurs" dans le panneau latéral
2. Sélectionnez les indicateurs souhaités dans la liste
3. Configurez les paramètres de chaque indicateur si nécessaire
4. Cliquez sur "Appliquer" pour afficher les indicateurs sur le graphique

#### Timeframes et intervalles
1. Utilisez les boutons de timeframe (1j, 1s, 1m, 1a, etc.) pour changer la période affichée
2. Utilisez le sélecteur d'intervalle pour changer la granularité des données (1m, 5m, 15m, 1h, 1j, etc.)

### Concepts ICT

L'application intègre les concepts du Smart Money Concept (ICT) pour une analyse avancée.

#### Affichage des zones ICT
1. Cliquez sur le bouton "ICT" dans le panneau latéral
2. Sélectionnez les concepts ICT souhaités (Fair Value Gaps, Order Blocks, etc.)
3. Configurez les paramètres si nécessaire
4. Cliquez sur "Appliquer" pour afficher les zones sur le graphique

#### Interprétation des zones ICT
Chaque zone ICT est accompagnée d'une bulle d'information accessible en cliquant sur l'icône "i" :
- **Fair Value Gaps (FVG)** : Zones de déséquilibre de prix qui tendent à être comblées
- **Order Blocks** : Zones où les institutions ont placé des ordres importants
- **Liquidity** : Niveaux où se concentrent les ordres stop-loss
- **Equal Highs/Lows** : Niveaux où le prix a atteint le même sommet/creux plusieurs fois
- **Breaker Blocks** : Order Blocks qui ont été cassés puis retestés
- **Imbalance** : Zones de déséquilibre entre l'offre et la demande

### Gestion de portefeuille

Le module de gestion de portefeuille vous permet de suivre vos investissements et leurs performances.

#### Création d'un portefeuille
1. Accédez à l'onglet "Portefeuilles"
2. Cliquez sur "Nouveau portefeuille"
3. Entrez un nom et une description
4. Cliquez sur "Créer"

#### Ajout de transactions
1. Sélectionnez un portefeuille dans la liste
2. Cliquez sur "Ajouter une transaction"
3. Sélectionnez le type de transaction (achat/vente)
4. Entrez le symbole de l'actif, la quantité, le prix et la date
5. Cliquez sur "Enregistrer"

#### Suivi des performances
1. Sélectionnez un portefeuille dans la liste
2. Consultez le tableau de bord du portefeuille pour voir :
   - La valeur totale
   - La performance globale
   - La répartition des actifs
   - L'historique des performances

#### Gestion des favoris
1. Recherchez un actif
2. Cliquez sur l'icône "étoile" pour l'ajouter à vos favoris
3. Accédez à l'onglet "Favoris" pour voir tous vos actifs favoris

### Alertes

Le système d'alertes vous permet d'être notifié lorsque certaines conditions sont remplies.

#### Création d'une alerte
1. Accédez à l'onglet "Alertes"
2. Cliquez sur "Nouvelle alerte"
3. Sélectionnez l'actif concerné
4. Choisissez le type d'alerte :
   - **Prix** : Alerte lorsque le prix atteint un certain niveau
   - **Zone ICT** : Alerte lorsque le prix entre dans une zone ICT
   - **Indicateur** : Alerte basée sur un indicateur technique
5. Configurez les conditions de l'alerte
6. Choisissez si l'alerte doit être répétable
7. Cliquez sur "Créer"

#### Configuration des canaux de notification
1. Accédez à l'onglet "Paramètres"
2. Sélectionnez "Notifications"
3. Activez ou désactivez les canaux souhaités (email, Telegram, WhatsApp)
4. Configurez les paramètres de chaque canal
5. Cliquez sur "Enregistrer"

## Dépannage

### Problèmes courants

#### L'application ne démarre pas
- Vérifiez que tous les services Docker sont en cours d'exécution : `docker-compose ps`
- Consultez les logs : `docker-compose logs`
- Vérifiez que les ports ne sont pas déjà utilisés par d'autres applications

#### Impossible de se connecter à la base de données
- Vérifiez les variables d'environnement de connexion à la base de données
- Assurez-vous que PostgreSQL est en cours d'exécution
- Vérifiez que la base de données existe : `psql -l`

#### Les notifications ne fonctionnent pas
- Vérifiez les variables d'environnement pour les services de notification
- Assurez-vous que les services externes (SMTP, Telegram) sont accessibles
- Consultez les logs pour les erreurs spécifiques

### Logs

#### Logs Docker
```bash
# Tous les services
docker-compose logs

# Service spécifique
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db
```

#### Logs Backend
Les logs du backend sont disponibles dans la console où le serveur est exécuté ou dans les logs Docker.

#### Logs Frontend
Les logs du frontend sont disponibles dans la console du navigateur (F12 > Console) ou dans les logs Docker.
