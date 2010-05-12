#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) Daniel Lombraña González
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
import sys
import random
import ConfigParser
from os import system
from os import path
from string import strip, split, atoi, upper
from ftplib import FTP

# Changes de wallpaper for Gnome. You only have to select the soft link: Wallpaper that this script generates. Each time you enter in your gnome session, you will see the soft link as the background.
# The best way for see the effect is adding one line like this in cron:
# @reboot /home/user/Wallpapers/cambiar.py
# If you want to have the wallpapers in other location, change the next variable to another Folder in your Home folder.

#Resolution = [1024,768]
Folder = "Wallpapers"   # Where it sould be the wallpapers and this script
WallpapersFile = ".wallpapers" # This file has the list of the wallpapers that are in the server art.gnome.org
if len(sys.argv)> 1:
    options = sys.argv[1]
else:
    options = ''

def get_this_files(wallpapers,type):
    """Returns a list with the names of the wallpaper that has the type: type"""
    aux = []
    if (type != "ALL"):
        for file in wallpapers:
            if file.count(type)>0:
                aux.append(file)
        return(aux)
    else:
        # As the list is ordered by type, we shuffle it in order to create an unshorted list of backgrounds
        random.shuffle(wallpapers)
        return(wallpapers)

def multiple_resolutions(wallpapers,resolution):
    """Returns a list with the names of the wallpaper that has several resolutions"""
    # One file has multiple resolutions when has a '_' in the name.
    list = []
    list_names = []
    for file in wallpapers:
        if file.count('_')>0: # the image has several resolutions
            res = split(file,'_')
            res = split(res[1],'.')
            res = split(res[0],'x')
            if (len(res)>=2):
                res[0] = atoi(res[0])
                res[1] = atoi(res[1])
                # We check if the file has the same or less resolution, and if the image has
                # several resolutions with the same name we only get one.
                if res[0]<= resolution[0] and res[1]<=resolution[1]:
                    name = split(file,'-')
                    name = split(name[1],'_')
                    list_names.append(name[0])
                    if list_names.count(name[0])<2:
                        list.append(file)
            else:
                name = split(file,'.')
                list_names.append(name[0])
                # The same as before, but now for images that are the same but with different extensions .png or .jpg
                if list_names.count(name[0]) < 2:
                    list.append(file)
        else:
            list.append(file)
    return list


# Generation of the path of Wallpapers
Wallpapers= os.path.join(os.path.expanduser( "~"), Folder)
ListWallpapersPath = os.path.join(Wallpapers,WallpapersFile)

# First we check if exists the file .wallpaperrc, if not we not run the progam and print an error, else we get the values and run it.
if not os.path.exists(".wallpaperrc"):
    print "ERROR: the file .wallpaperrc dont exists, create it"
else:
    config = ConfigParser.ConfigParser()
    config.read(".wallpaperrc")
    Options={}
    for section in config.sections():
        for op in config.options(section):
            value = config.get(section,op)
            if op=='type': Options[op]=upper(value) # This is done, because in art.gnome.org the type of the wallpaper is set in uppercase letters.
            else: Options[op]=value
    print Options

# FTP
ftp = FTP( 'ftp.gnome.org')
ftp.login( )
# Change the root directory for image files
ftp.cwd('./Public/GNOME/teams/art.gnome.org/backgrounds/')
list_files = ftp.nlst( )
# If we have passed the option -r from --random we select a random file, else we write the list of images if before no exists this file.
if (options == '-r'):
    file = random.choice(list_files)
else:
    # If not exists the list, then is the first time we execute this option, so we get the last wallpaper and write the others to a list for the next execution
    if not os.path.exists(ListWallpapersPath):
        Flist = open(ListWallpapersPath,'w')
        if Options['type']!='all': list_files = get_this_files(list_files,Options['type'])
        list_resolutions = multiple_resolutions(list_files,Options['resolution'])
        file = list_resolutions.pop()
        for i in list_resolutions:
            Flist.write(i + '\n')
        Flist.close()
    else:
        Flist = open(ListWallpapersPath,'r')
        list_files = Flist.readlines()
        Flist.close()
        # If we get the last wallpaper in the list we have to delete the file to create again the list.
        if len(list_files)!=1:
            file = strip(list_files.pop())
            Flist = open(ListWallpapersPath,'w')
            for i in list_files:
                Flist.write(strip(i) +'\n')
            Flist.close()
        else:   
            file = strip(list_files.pop())
            os.remove(ListWallpapersPath)
    
print "Downloading " + file
local_file = open( os.path.join(Wallpapers,file),'wb')
# We must download the selected file
ftp.retrbinary('RETR ' + file,local_file.write, 1024)
ftp.close( )
background = file
# First we delete the old image. This is because the Folder will be increase its size if we dont delete nothing.
files = os.listdir(Wallpapers)
# We check if this is the first time that we execute this script, if so then we dont need to erase the previous image or background.
if files.count( 'Wallpaper') > 0:
    os.remove(os.readlink(os.path.join(Wallpapers,'Wallpaper')))
    # Here we change the old softlink to the newer one
    os.remove(os.path.join(Wallpapers,'Wallpaper'))
os.symlink(os.path.join(Wallpapers,background), os.path.join(Wallpapers,'Wallpaper'))
