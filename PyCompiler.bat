:: A very good python compiler
@echo off
setlocal enabledelayedexpansion

:: Compiler Options
set "iconpath=src/assets/icon.ico"
set "pyFile=src/main.py"
set "name=ModManager"
set "target_dir_name=target"
set "bin_dis=./%target_dir_name%/bin"
set "temp_dis=./%target_dir_name%/build"

:: The script that runs the compiler
set PYTHONOPTIMIZE=1 && pyinstaller ^
    %pyFile% ^
    --name %name% ^
    --distpath %bin_dis% ^
    --workpath %temp_dis% ^
    --clean ^
    --key=$2y$19$DP7Ad7mckjM.Wwxtl9uCBuHDDyb/B5iKab4LS3EXNqVi3ueCTBike ^
    --onefile ^
    --icon=%iconpath% ^
    --win-private-assemblies ^
    --win-no-prefer-redirects ^
    --uac-admin

:: Yes I know useless stuff but at least it's cool
set "appPath=%bin_dis%/%name%.exe"
for %%F in ("%appPath%") do set "fileSizeBytes=%%~zF"
:: Calculate file size in KB, MB, and GB using PowerShell
for /f "delims=" %%A in ('powershell "$fileSizeKB=[math]::Round($fileSizeBytes / 1KB, 2); $fileSizeMB=[math]::Round($fileSizeBytes / 1MB, 2); $fileSizeGB=[math]::Round($fileSizeBytes / 1GB, 2); Write-Host $fileSizeBytes, $fileSizeKB, $fileSizeMB, $fileSizeGB"') do (
    set "fileSizeInfo=%%A"
)
:: Parse the output from PowerShell
for /f "tokens=1-4" %%B in ("!fileSizeInfo!") do (
    set "fileSizeB=%%B"
    set "fileSizeKB=%%C"
    set "fileSizeMB=%%D"
    set "fileSizeGB=%%E"
)
:: Convert file size to other units
set /a "fileSizeKB=fileSizeBytes / 1024"
set /a "fileSizeMB=fileSizeBytes / 1048576"
set /a "fileSizeGB=fileSizeBytes / 1073741824"
:: Display file size
echo ^

Size of %name%.exe is:
echo %fileSizeGB% Gigabytes
echo %fileSizeMB% Megabytes
echo %fileSizeKB% Kilobytes
echo %fileSizeBytes% Bytes ^
 
:: Run the compiled Python executable
"%appPath%"

endlocal