#!/bin/zsh
if [ -f .env ]; then
    echo ".env exists!"
else
    echo ".env does not exist!"
    cp .env_example .env
    echo ".env created using .env_example!"
    exit 1
fi

EXAMPLE_SETTINGS=$(cat .env_example)
SETTINGS=$(cat .env)

if [ "$EXAMPLE_SETTINGS" = "$SETTINGS" ]; then
    echo ".env_example is UP TO DATE!"
    exit 0
else
    echo "Updating .env_example from .env!"
    cp .env .env_example
    exit 1
fi
