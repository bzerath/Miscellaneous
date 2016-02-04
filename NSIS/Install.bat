cd ..

if exist Clean\ del Clean\ /q /s

rem D'ABORD ON COPIE TOUS LES FICHIERS DANS UN DOSSIER PROPRE, PUIS ON TRAVAILLE DESSUS (compilation et installer)

rem Copie des dossiers en excluant les .pyc
echo .pyc > excludedfileslist.txt
xcopy Csv 		Clean\Csv\ 		/E
xcopy Extra 	Clean\Extra\ 	/E
xcopy Libs 	    Clean\Libs\ 	/E /exclude:excludedfileslist.txt
xcopy Servers 	Clean\Servers\ 	/E /exclude:excludedfileslist.txt
xcopy Xml 		Clean\Xml\ 		/E
del excludedfileslist.txt

rem Copie les fichiers de la racine
xcopy Launcher.bat 			Clean\
xcopy Main.py 						Clean\			
xcopy "README LiteAts_U500.txt" 	Clean\
xcopy Configuration.ini 			Clean\
xcopy setup.py 						Clean\

rem Maintenant on a un dossier tout propre (dont on peut se servir plus tard, pour le zipper par exemple).

rem Compile LiteATS
cd Clean
C://Python27//python setup.py py2exe

rem Rapatrie les fichiers dont on a besoin dans /dist pour que le logiciel marche...
xcopy Xml 		dist\Xml\ 		/E
xcopy Extra 	dist\Extra\ 	/E
xcopy Configuration.ini 	dist\
xcopy "README.txt" 	dist\

rem Creation de l'installer
cd ..
"C:\Program Files (x86)\NSIS\makensis" /V2 ".\NSI requirements\Setup_Genius_general.nsi"

xcopy ".\NSI requirements\Setup.exe"	Clean\
del ".\NSI requirements\Setup.exe"


pause