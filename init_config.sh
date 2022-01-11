#!/bin/zsh
cp .env_example .env
cp .secrets_example.toml .secrets.toml
dir=$HOME/.docker/database/mongodb_fastapi_base
echo "Created $dir to store docker volumes!"
mkdir -p $HOME/.docker/database/mongodb_fastapi_base
