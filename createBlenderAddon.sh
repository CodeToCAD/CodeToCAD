#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )" # copypasta from https://stackoverflow.com/a/4774063/

cd "$SCRIPT_DIR"

BLENDER_ADDON_PATH="./CodeToCADBlenderAddon"
OUTPUT_FILE_PATH="./CodeToCADBlenderAddon.zip"

# Clean up existing files
echo "Cleaning up existing files."

for  file in $(find ./CodeToCAD -name '*__pycache__') ; do
rm -rf $file
done
for  file in $(find ./providers/blender/ -name '*__pycache__') ; do
rm -rf $file
done
rm -rf $BLENDER_ADDON_PATH
rm $OUTPUT_FILE_PATH


# Copy new files
echo "Copy new files."

mkdir $BLENDER_ADDON_PATH
mkdir $BLENDER_ADDON_PATH/blenderProvider
cp -r ./providers/blender/blenderProvider $BLENDER_ADDON_PATH
cp -r ./CodeToCAD $BLENDER_ADDON_PATH/
cp -f ./providers/blender/CodeToCADBlenderAddon.py $BLENDER_ADDON_PATH/__init__.py

# Write version string
echo "Writing version string."

GIT_EPOCH=$(git show -s --format=%ct HEAD)

if [[ "$OSTYPE" == "darwin"* ]]; then
sed -i '' "s/),  # patch_version marker do not remove/, $GIT_EPOCH),/g" $BLENDER_ADDON_PATH/__init__.py
else
sed "s/),  # patch_version marker do not remove/, $GIT_EPOCH),/g" $BLENDER_ADDON_PATH/__init__.py
fi

# Zip the BlenderAddon folder
echo "Zipping BlenderAddon folder."

zip -q -r $OUTPUT_FILE_PATH $BLENDER_ADDON_PATH