#!/usr/bin/env bash

POSTGRES_PASSWORD=$(openssl rand -base64 12)
POSTGRES_USER=postgres
POSTGRES_DB=twitn

0>.env
echo "DATABASE_URL=postgresql+psycopg://$POSTGRES_USER:$POSTGRES_PASSWORD@db:5432/$POSTGRES_DB" > .env
echo "POSTGRES_PASSWORD=$POSTGRES_PASSWORD" >> .env
echo "POSTGRES_USER=$POSTGRES_USER" >> .env
echo "POSTGRES_DB=$POSTGRES_DB" >> .env