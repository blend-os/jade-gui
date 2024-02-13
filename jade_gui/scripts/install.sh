#!/usr/bin/bash

echo | tee /tmp/jade-gui-output.txt &>/dev/null
echo "Configuring your system." | tee -a /tmp/jade-gui-output.txt
sudo blend-postinst config ~/.config/jade.json 2>/dev/null | tee -a /tmp/jade-gui-output.txt
