#!/bin/bash
echo "-------------------"
echo "Generate file .env"
echo "-------------------"

# Generate symbol string
for symbol in {A..Z} {a..z} {0..9}; do
  SYMBOLS=$SYMBOLS$symbol
done
SYMBOLS=$SYMBOLS'!@#$%&*()?/\[]{}-+_=<>.,'


# Generate username
for (( i=1; i <= 8; i++ )); do
usr=$usr${SYMBOLS:$(expr $RANDOM % ${#SYMBOLS}):1}
done


# Generate password
for (( i=1; i <= 16; i++ )); do
pass=$pass${SYMBOLS:$(expr $RANDOM % ${#SYMBOLS}):1}
done


echo "POSTGRES_USER = \"usr_$usr\"" | tee .env
echo "POSTGRES_PASSWORD = \"$pass\"" | tee -a .env
echo "POSTGRES_HOST = \"test_app_db_1\"" | tee -a .env
echo "POSTGRES_PORT = \"5432\"" | tee -a .env
echo "POSTGRES_DB = \"testdb\"" | tee -a .env

cp .env app/

