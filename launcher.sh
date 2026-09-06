#!/bin/bash
# AUTO-UPDATER
cd /home/suraj/.gemini/antigravity/scratch/heavy_suite/zero-physics-mac
git pull origin main --quiet
python3 zero_physics_gui.py
