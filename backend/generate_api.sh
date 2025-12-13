#!/bin/bash
source .venv/Scripts/activate
pip install openapi-generator-cli > /dev/null 2>&1
openapi-generator-cli generate -i resources/api/v1/draw.yaml -g python-fastapi -o generated/
if [ -d "openapi_server" ]; then
    rm -rf openapi_server
fi
cp -r generated/src/openapi_server openapi_server
grep -v "uvloop==0.21.0" generated/requirements.txt > generated/requirements_clean.txt
mv generated/requirements_clean.txt generated/requirements.txt
cp generated/requirements.txt openapi_server/requirements.txt
pip install -r "openapi_server/requirements.txt" > /dev/null 2>&1
rm -rf generated
