#!/bin/sh

mkdir -p ~/.local/share/gedit/plugins
cp -r gedit-hide-onsave* ~/.local/share/gedit/plugins

echo "Gedit OnSave installed! Now restart Gedit and active the plugin in Edit > Preferences."
