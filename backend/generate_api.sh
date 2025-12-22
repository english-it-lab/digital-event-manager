#!/bin/sh
set -e

if [ -f ".venv/bin/activate" ]; then
    . .venv/bin/activate
elif [ -f ".venv/Scripts/activate" ]; then
    . .venv/Scripts/activate
fi

pip install openapi-generator-cli

for yaml_file in resources/api/v1/*.yaml; do
    openapi-generator-cli generate \
        -i "$yaml_file" \
        -g python-fastapi \
        -o generated/
done

if [ -d "openapi_server" ]; then
    rm -rf openapi_server
fi

cp -r generated/src/openapi_server openapi_server
grep -v "uvloop==0.21.0" generated/requirements.txt > openapi_server/requirements.txt
pip install -r openapi_server/requirements.txt

rm -rf generated