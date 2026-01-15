# Le backend de Twi'TN

Ce dernier est un projet `uv` - vous devez utiliser uv pour gérer vos dépendances et votre venv.

> Assurez vous d'avoir bien installé `uv`

Créez votre venv avec `uv venv`
Puis `. .venv/bin/activate` pour l'activer, suivi de `uv sync` pour installer le dépendances.

Utilisez `flask run` pour lancer l'environment de developement qui sera disponible à http://127.0.0.1:5000

## Linting 

Pour re-formater le code on utilise `ruff` - `ruff check (--fix)` pour vérifier et `ruff format` pour reformater

## Mise à jour de spec OpenAPI

Après une mise à jour il faut faire : `./export_openapi_spec.py`
