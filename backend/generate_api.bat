@echo off
setlocal

call .venv\Scripts\activate
pip install openapi-generator-cli >nul 2>&1
openapi-generator-cli generate -i resources/api/v1/draw.yaml -g python-fastapi -o generated/
if exist openapi_server rmdir /s /q openapi_server
xcopy /E /I /Y generated\src\openapi_server openapi_server
findstr /v /c:"uvloop==0.21.0" "generated\requirements.txt" > "generated\requirements_clean.txt"
move /y "generated\requirements_clean.txt" "generated\requirements.txt"
copy /y "generated\requirements.txt" "openapi_server\requirements.txt"
pip install -r "openapi_server\requirements.txt" >nul 2>&1
rmdir /s /q generated
