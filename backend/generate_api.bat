@echo off
setlocal enabledelayedexpansion

call .venv\Scripts\activate.bat
pip install openapi-generator-cli

for %%f in (resources\api\v1\*.yaml) do (
    set "file=%%~nf"
    
    openapi-generator-cli generate -i %%f -g python-fastapi -o generated_!file!\
    
    if exist openapi_server_!file!\ rd /s /q openapi_server_!file!\
    
    xcopy generated_!file!\src\openapi_server openapi_server_!file!\ /e /i /q
    
    findstr /v "uvloop==0.21.0" generated_!file!\requirements.txt > openapi_server_!file!\requirements.txt
    
    pip install -r openapi_server_!file!\requirements.txt
    
    rd /s /q generated_!file!\
)