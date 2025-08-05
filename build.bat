@echo off
cd /d %~dp0
rmdir /s /q build
rmdir /s /q dist
del linkedin_autopost.spec

python -m PyInstaller --onefile --name linkedin_autopost ^
--add-data "app;app" ^
--add-data ".env;." ^
--collect-all fastapi ^
--collect-all uvicorn ^
--collect-all pydantic ^
--collect-all sqlalchemy ^
--collect-all apscheduler ^
--collect-all dotenv ^
--collect-all requests ^
--collect-all openai ^
start_app.py

pause
