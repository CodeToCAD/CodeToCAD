#!/usr/bin/env bash

BLENDER_ADDON_PATH="./CodeToCADBlenderAddon/"

rm -rf ./providers/blender/__pycache__
rm -rf ./$BLENDER_ADDON_PATH
cp -r ./providers/blender $BLENDER_ADDON_PATH
cp -r ./CodeToCAD $BLENDER_ADDON_PATH/

mv -f $BLENDER_ADDON_PATH/CodeToCADBlenderAddon.py $BLENDER_ADDON_PATH/__init__.py
GIT_EPOCH=$(git show -s --format=%ct HEAD)

if [[ "$OSTYPE" == "darwin"* ]]; then
sed -i '' "s/),  # patch_version marker do not remove/, $GIT_EPOCH),/g" $BLENDER_ADDON_PATH/__init__.py
else
sed "s/),  # patch_version marker do not remove/, $GIT_EPOCH),/g" $BLENDER_ADDON_PATH/__init__.py
fi

rm CodeToCADBlenderAddon.zip

zip -r CodeToCADBlenderAddon.zip $BLENDER_ADDON_PATH/