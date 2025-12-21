#!/bin/sh
set -e

source .venv/Scripts/activate
pip install openapi-generator-cli

for yaml_file in resources/api/v1/*.yaml; do
    file=$(basename "$yaml_file" .yaml)
    
    openapi-generator-cli generate \
        -i "$yaml_file" \
        -g python-fastapi \
        -o generated_${file}/
    
    if [ -d "openapi_server_${file}" ]; then
        rm -rf openapi_server_${file}
    fi
    
    cp -r generated_${file}/src/openapi_server openapi_server_${file}
    
    grep -v "uvloop==0.21.0" generated_${file}/requirements.txt > generated_${file}/requirements_clean.txt
    mv generated_${file}/requirements_clean.txt generated_${file}/requirements.txt
    cp generated_${file}/requirements.txt openapi_server_${file}/requirements.txt
    
    pip install -r "openapi_server_${file}/requirements.txt"
    
    rm -rf generated_${file}
done