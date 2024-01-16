@echo off

set FUSION_ADDON_PATH=CodeToCADFusionAddon

if not exist %FUSION_ADDON_PATH% mkdir %FUSION_ADDON_PATH%

for /d /r %%i in (*__pycache__*) do @rmdir /s /q "%%i"

xcopy /S /Y providers\fusion360\fusion360_provider\* %FUSION_ADDON_PATH%\providers\fusion360\fusion360_provider\*
xcopy /S /Y codetocad\* %FUSION_ADDON_PATH%\*
copy providers\fusion360\fusion360_addon.py %FUSION_ADDON_PATH%\__init__.py
copy examples\fusion360.py "%appdata%\Autodesk\Autodesk Fusion 360\API\Scripts\fusion360.py"
xcopy /S /Y %FUSION_ADDON_PATH%\ "%appdata%\..\Local\Autodesk\webdeploy\production\b0c303e70bd97cfdc195adab65922cfeffcb363a\Api\Python\packages\codetocad\"

rmdir %FUSION_ADDON_PATH% /s /q
