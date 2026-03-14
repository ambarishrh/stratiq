@echo off
echo Stopping StratIQ...
docker stop stratiq && docker rm stratiq
echo Done. Your data is preserved.
pause
