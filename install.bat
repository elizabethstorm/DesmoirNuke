@echo off
setlocal

:: Define Python version and architecture
set PYTHON_VERSION=3.10.0
set PYTHON_ARCH=amd64

:: Define download URL
set PYTHON_DOWNLOAD_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-amd64.exe

:: Download Python installer
powershell -Command "Invoke-WebRequest %PYTHON_DOWNLOAD_URL% -OutFile python-installer.exe"

:: Run Python installer
start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

:: Clean up
del python-installer.exe

endlocal