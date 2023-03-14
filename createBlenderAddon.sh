
BLENDER_ADDON_PATH="./CodeToCADBlenderAddon/"

rm -rf ./providers/blender/__pycache__
rm -rf ./$BLENDER_ADDON_PATH
cp -r ./providers/blender $BLENDER_ADDON_PATH
cp -r ./CodeToCAD $BLENDER_ADDON_PATH/

mv -f $BLENDER_ADDON_PATH/CodeToCADBlenderAddon.py $BLENDER_ADDON_PATH/__init__.py

rm CodeToCADBlenderAddon.zip

zip -r CodeToCADBlenderAddon.zip $BLENDER_ADDON_PATH/