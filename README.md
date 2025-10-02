# Finance Analysis Platform

Une application web complète d'analyse et d'alerte boursière, intégrant des outils d'analyse financière avancée, le concept ICT (Smart Money Concept), et un système d'alertes multicanal.

## Fonctionnalités principales

- **Analyse technique avancée** : Indicateurs classiques (EMA, MA, RSI, MACD, etc.) et concepts ICT (Fair Value Gaps, Order Blocks, etc.)
- **Gestion de portefeuille** : Suivi des actifs, favoris, performances et métriques de risque
- **Système d'alertes** : Notifications via email, Telegram et WhatsApp
- **Multi-actifs** : Actions, indices, cryptomonnaies, forex, matières premières
- **Interface utilisateur intuitive** : Bulles d'information explicatives pour chaque graphique
- **Authentification sécurisée** : Système complet de gestion des utilisateurs

## Architecture technique

- **Backend** : Python FastAPI, PostgreSQL, Redis
- **Frontend** : Vue.js 3, TradingView Lightweight Charts, Tailwind CSS
- **Déploiement** : Docker, Docker Compose
- **Intégrations** : APIs financières, Telegram, Email, WhatsApp

## Prérequis

- Docker et Docker Compose
- Un compte Telegram Bot (pour les notifications Telegram)
- Un compte email (pour les notifications par email)

## Installation

1. Cloner le dépôt :
   ```bash
   git clone https://github.com/votre-username/finance-app.git
   cd finance-app
   ```

2. Configurer les variables d'environnement :
   Créez un fichier `.env` à la racine du projet avec les variables suivantes :
   ```
   SECRET_KEY=votre-clé-secrète-pour-jwt
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USERNAME=votre-email@gmail.com
   EMAIL_PASSWORD=votre-mot-de-passe-email
   TELEGRAM_BOT_TOKEN=votre-token-telegram-bot
   ```

3. Lancer l'application avec Docker Compose :
   ```bash
   docker-compose up -d
   ```

4. Accéder à l'application :
   - Frontend : http://localhost
   - API Backend : http://localhost:8000
   - Documentation API : http://localhost:8000/docs
   - pgAdmin (gestion de la base de données) : http://localhost:5050

## Configuration des notifications

### Email
Les notifications par email sont activées par défaut. Assurez-vous de configurer correctement les variables d'environnement EMAIL_*.

### Telegram
1. Créez un bot Telegram via [@BotFather](https://t.me/botfather)
2. Obtenez le token du bot et configurez-le dans la variable d'environnement TELEGRAM_BOT_TOKEN
3. Démarrez une conversation avec votre bot
4. Dans l'application, activez les notifications Telegram et entrez votre ID de chat

### WhatsApp
L'intégration WhatsApp nécessite un compte WhatsApp Business API. Consultez la documentation pour plus de détails sur la configuration.

## Utilisation

### Création de compte
1. Accédez à l'application via http://localhost
2. Cliquez sur "S'inscrire" et créez un compte avec votre email
3. Connectez-vous avec vos identifiants

### Analyse de marché
1. Utilisez la barre de recherche pour trouver un actif
2. Sélectionnez les indicateurs techniques ou concepts ICT à afficher
3. Utilisez les outils de dessin pour analyser le graphique
4. Consultez les bulles d'information pour comprendre chaque indicateur

### Gestion de portefeuille
1. Créez un nouveau portefeuille
2. Ajoutez des transactions (achat/vente)
3. Suivez les performances de votre portefeuille
4. Ajoutez des actifs à vos favoris pour un accès rapide

### Configuration des alertes
1. Définissez des conditions d'alerte (prix, zones ICT, indicateurs)
2. Configurez vos canaux de notification préférés
3. Activez/désactivez les alertes selon vos besoins

## API Backend

L'API FastAPI exposée via `/api/v1` propose plusieurs groupes d'endpoints :

- **/users** : inscription, authentification JWT, consultation et mise à jour des préférences de notification.
- **/portfolios** : création, consultation, mise à jour et suppression de portefeuilles ainsi que gestion des transactions et calcul des performances.
- **/alerts** : gestion complète des alertes sur les actifs suivis (création, lecture, modification, suppression).
- **/analysis** : récupération des données de marché, calcul d'indicateurs techniques et analyse ICT sur les actifs financiers.

Chaque route applique les protections d'authentification et s'appuie sur les services métiers pour garantir la cohérence des données (PostgreSQL) et l'accès aux APIs financières externes.

## Développement

### Structure du projet
```
finance-app/
├── backend/              # API FastAPI
│   ├── app/
│   │   ├── api/          # Routes API
│   │   ├── core/         # Configuration
│   │   ├── db/           # Base de données
│   │   ├── models/       # Modèles SQLAlchemy
│   │   ├── schemas/      # Schémas Pydantic
│   │   ├── services/     # Services métier
│   │   └── main.py       # Point d'entrée
│   ├── requirements.txt  # Dépendances Python
│   └── Dockerfile        # Configuration Docker
├── frontend/             # Application Vue.js
│   ├── src/
│   │   ├── assets/       # Ressources statiques
│   │   ├── components/   # Composants Vue
│   │   ├── views/        # Pages
│   │   ├── store/        # État global
│   │   └── main.js       # Point d'entrée
│   ├── package.json      # Dépendances Node.js
│   └── Dockerfile        # Configuration Docker
├── docs/                 # Documentation
├── docker-compose.yml    # Configuration Docker Compose
└── README.md             # Documentation principale
```

### Exécution en mode développement

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run serve
```

## Contribution

Les contributions sont les bienvenues ! Veuillez suivre ces étapes :
1. Forkez le dépôt
2. Créez une branche pour votre fonctionnalité
3. Committez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## Contact

Pour toute question ou suggestion, veuillez ouvrir une issue sur GitHub ou contacter l'équipe de développement.
