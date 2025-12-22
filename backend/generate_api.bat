@echo off

if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)

pip install openapi-generator-cli

for %%f in (resources\api\v1\*.yaml) do (
    openapi-generator-cli generate -i %%f -g python-fastapi -o generated\
)

if exist openapi_server\ rd /s /q openapi_server

xcopy generated\src\openapi_server openapi_server\ /e /i /q
findstr /v "uvloop==0.21.0" generated\requirements.txt > openapi_server\requirements.txt
pip install -r openapi_server\requirements.txt

rd /s /q generated