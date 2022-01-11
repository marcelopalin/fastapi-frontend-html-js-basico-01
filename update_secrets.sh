#!/bin/zsh
if [ -f .secrets.toml ]; then
    echo ".secrets.toml exists!"
else
    echo "secrets.toml does not exist!"
    cp .secrets_example.toml .secrets.toml
    echo ".secrets.toml created!"
    exit 1
fi

SECRETS_EXAMPLE_CONTENT=$(cat .secrets_example.toml)
SECRETS_CONTENT=$(cat .secrets.toml)

if [ "$SECRETS_EXAMPLE_CONTENT" = "$SECRETS_CONTENT" ]; then
    echo ".secrets_example.toml já está atualizado!"
    exit 0
else
    echo "Atualizando .secrets_example.toml!"
    cp .secrets.toml .secrets_example.toml
    exit 1
fi
