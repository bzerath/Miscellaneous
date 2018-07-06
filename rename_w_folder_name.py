# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # Everything is UTF-8
import os

path_folder = ""

if __name__ == "__main__":
    print (os.listdir(path_folder))
    folders = os.listdir(path_folder)
    for folder in folders:
        if os.path.isdir(os.path.join(path_folder, folder)):
            for fichier in os.listdir(os.path.join(path_folder, folder)):
                os.rename(os.path.join(path_folder, folder, fichier),
                          os.path.join(path_folder, folder+"_"+fichier))
                # Cancel :
                # len_entete = len(folder + "_")
                # os.rename(os.path.join(path_folder, folder, fichier),
                #           os.path.join(path_folder, folder, fichier[len_entete:]))


