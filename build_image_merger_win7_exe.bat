@echo off
cd /d "%~dp0"

python --version
python -m pip install --upgrade pip
python -m pip install -r requirements-win7.txt

rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del /q ImageMerger_Win7.spec 2>nul

python -m PyInstaller --onefile --windowed --name ImageMerger_Win7 image_merger_win7.py

echo.
echo Finished. EXE location:
echo %~dp0dist\ImageMerger_Win7.exe
pause
