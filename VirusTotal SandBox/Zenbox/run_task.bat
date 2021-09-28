@echo off

taskkill /F /IM python.exe 2>nul
taskkill /F /IM py.exe 2>nul

timeout /t 2 /nobreak >nul

cd c:\mydownload & vex2_run_task.exe

@echo on
