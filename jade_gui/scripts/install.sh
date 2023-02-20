#!/usr/bin/bash
echo "Running reflector to sort for fastest mirrors" | tee -a /tmp/jade-gui-output.txt
pkexec reflector --latest 5 --sort rate --save /etc/pacman.d/mirrorlist | tee -a /tmp/jade-gui-output.txt
pkexec crystal-jade config ~/.config/jade.json | tee -a /tmp/jade-gui-output.txt
