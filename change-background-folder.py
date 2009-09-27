#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) Daniel Lombraña González.
#
# This file is part of changewallpaper.
# 
# changewallpaper is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# changewallpaper is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with changewallpaper.  If not, see <http://www.gnu.org/licenses/>.

import os
import random
from os import system
from os import path

# Changes de wallpaper for Gnome. You only have to select the soft link: Wallpaper that this script generates. Each time you enter in your gnome session, you will see the soft link as the background.
# The best way for see the effect is adding one line like this in cron:
# @reboot /home/user/Wallpapers/cambiar.py
# If you want to have the wallpapers in other location, change the next variable to another Folder in your Home folder.

Folder = "Wallpapers"   # Where it sould be the wallpapers and this script

# Generation of the path of Wallpapers
Wallpapers= os.path.join(os.path.expanduser( "~"), Folder)

# We get the different files in the folder, and choose one randomly
files = os.listdir(Wallpapers)
# We remove the script and the soft link from the candidates to be selected
files.remove('cambiar.py')
if os.path.isfile(os.path.join(Wallpapers,'Wallpaper')):
    files.remove('Wallpaper')
background = random.choice(files)
# Here we change the old softlink to the newer one
os.remove(os.path.join(Wallpapers,'Wallpaper'))
os.symlink(os.path.join(Wallpapers,background), os.path.join(Wallpapers,'Wallpaper'))

