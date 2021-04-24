import win32api
import os
import glob
from pprint import pprint


drives = win32api.GetLogicalDriveStrings().split('\000')[:-1]
print(drives)
extensions = {
 '.7z',
 '.BMP',
 '.DOC',
 '.DOCX',
 '.EXE',
 '.Exe',
 '.JPG',
 '.JSON',
 '.Json',
 '.MOV',
 '.MP3',
 '.MP4',
 '.MPG',
 '.Mp3',
 '.PDF',
 '.PNG',
 '.PPT',
 '.PPTX',
 '.Sims3Pack',
 '.XLS',
 '.XLSX',
 '.XML',
 '.apk',
 # '.bin',
 '.bmp',
 '.bz2',
 '.cbz',
 # '.dLL',
 # '.dll',
 '.doc',
 '.docx',
 # '.exe',
 '.flac',
 '.geojson',
 '.h264',
 '.jpeg',
 '.jpg',
 '.m3u',
 '.m3u8',
 '.m4a',
 '.m4v',
 '.mov',
 '.mp3',
 '.mp4',
 '.mpg',
 '.pdf',
 '.ppt',
 '.pptx',
 '.rar',
 '.sims3pack',
 '.tar',
 '.torrent',
 '.wav',
 '.webm',
 '.webp',
 '.world',
 '.xls',
 '.xlsx',
 '.xltx',
 '.xml',
 '.zip',
 '.zipmod'}

# drive = "F:\\"
# dossier = os.path.join(drive, "HS dx v3")
# drives = [dossier]

all_files = {}

for drive in drives:
    if "G" in drive:
        continue
    for file in glob.glob(drive + "\\**\\*.*", recursive=True):
        try:
            if os.path.isfile(file) and os.path.splitext(file)[-1] in extensions:
                size = os.path.getsize(file)
                if size > 1000000:
                    if (os.path.basename(file), size) not in all_files:
                        all_files[(os.path.basename(file), size)] = set()
                    all_files[(os.path.basename(file), size)].add(file)
        except FileNotFoundError:
            pass
    print(drive, len(all_files))

files_not_duplicated = set()
for key, value in all_files.items():
    if len(value) < 2:
        files_not_duplicated.add(key)
for f in files_not_duplicated:
    del(all_files[f])
print(len(all_files))
pprint(all_files, width=200)
