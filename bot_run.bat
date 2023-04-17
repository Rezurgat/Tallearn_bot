@echo off

call %~dp0Tallearn_bot\venv\Scripts\activate

cd %~dp0Tallearn_bot

set TOKEN=6254431019:AAEOKktpTE80krSXIu2p8T92TyYIDxQGCY4

python tallearn_bot.py

pause