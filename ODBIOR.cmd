@echo off
cd /d "%~dp0"
python inbox.py --open
if errorlevel 1 pause
