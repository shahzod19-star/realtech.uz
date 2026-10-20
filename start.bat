@echo off
title RealTech Uz Web Server
cd /d "%~dp0"
echo ==================================================
echo   RealTech Uz - Gadjetlar Batareya Tahlili
echo ==================================================
echo Brauzerda http://localhost:3000 ochilmoqda...
start http://localhost:3000
py server.py
pause
