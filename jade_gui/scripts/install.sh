#!/usr/bin/bash
echo "Running reflector to sort for fastest mirrors" | tee -a /tmp/jade-gui-output.txt
pkexec reflector --latest 5 --sort rate --save /etc/pacman.d/mirrorlist 2>/dev/null | tee -a /tmp/jade-gui-output.txt
pkexec blend-inst config ~/.config/jade.json | tee -a /tmp/jade-gui-output.txt
