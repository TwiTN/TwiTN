# Twi'TN

Twi’tn est un projet web inspiré de Twitter, conçu comme un réseau social interne pour les étudiants de Télécom Nancy.
Il permet aux utilisateurs de publier de courts messages, d’interagir entre eux et de suivre l’actualité de la communauté étudiante dans un environnement simple et moderne.

Ce projet a été réalisé dans le cadre du module WebBD, avec pour objectif de mettre en pratique les notions de développement web et de gestion de bases de données vues en cours : conception d’une application complète, interaction front-end / back-end, gestion des utilisateurs et persistance des données.

Twi’tn se veut à la fois un outil pédagogique et un prototype fonctionnel de réseau social, reproduisant certaines fonctionnalités clés de Twitter, tout en étant adapté au contexte de Télécom Nancy.

## Lancer le projet

> Avant de pouvoir lancer le projet il est nécessaire de générer le .env via le script [generate_dotenv.sh](generate_dotenv.sh)

Ensuite lancez cette commande :

```
docker compose up
```

> Le lancement de Twi'TN est également possible avec la commande `podman-compose up`

Vous pouvez désormais accéder à [Twi'TN](http://127.0.0.1:8000/)

## Poursuivre le développement

Ce dernier est un projet `uv` - vous devez utiliser uv pour gérer vos dépendances et votre venv.

> Assurez vous d'avoir bien installé `uv`

Créez votre venv avec `uv venv`
Puis `. .venv/bin/activate` pour l'activer, suivi de `uv sync` pour installer le dépendances.

Utilisez `flask run` pour lancer l'environment de developement qui sera disponible à http://127.0.0.1:5000


### Linting 

#### Python

Pour re-formater le code python on utilise `ruff` - `ruff check (--fix)` pour vérifier et `ruff format` pour reformater

#### JavaScript

Pour re-formater le code javascript on utilise `npm run lint`.

### Mise à jour de spec OpenAPI

Après une mise à jour il faut faire : `./export_openapi_spec.py`

### Swagger (OpenAPI)

Twi'TN utilise OpenAPI pour la définition des routes.

Un swagger est disponible à l'url : http://127.0.0.1:8000/openapi/swagger 