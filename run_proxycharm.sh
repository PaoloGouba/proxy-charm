#!/bin/bash

# Esegui lo script Python
python3 /Users/paologouba/Documents/Paolo/Goals/proxy-charm/src/main.py

# Aggiorna la repository su GitHub
cd /Users/paologouba/Documents/Paolo/Goals/proxy-charm
git add .
git commit -m "Daily update"
git push origin main
