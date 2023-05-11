#!/usr/bin/bash
echo | tee /tmp/jade-gui-output.txt &>/dev/null
echo "Starting installation with blend-inst..." | tee -a /tmp/jade-gui-output.txt
pkexec blend-inst config ~/.config/jade.json 2>&/dev/null | tee -a /tmp/jade-gui-output.txt
