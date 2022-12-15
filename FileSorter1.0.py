
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import os, os.path
import json
import time
import sys


class MyHandler(FileSystemEventHandler):
    def on_modified(itself, event):

        global x
        global first
        x = x + 1
        if x == 4:
            x = 1
            first = True
        
        for filename in os.listdir(folder_to_track):
            
            skip = False
            
            extension = os.path.splitext(filename)[1]
            if extension != ".part" or extension != ".crdownload" or extension != ".opdownload" or filename != "FileHandler.yaml" or filename != "FileSorter1.1.py" or filename != "FileSorter1.1.exe":
                if extension == ".jpg" or extension == ".png" or extension == ".tiff" or extension == ".gif" or extension == ".webp":
                    folderDestination = folder_to_track +'/Images'
                elif extension == ".mp4" or extension == ".mov" or extension == ".mpg":
                    folderDestination = folder_to_track + '/Videos'
                elif extension == ".pdf" or extension == ".docx" or extension == ".html" or extension == ".doc" or extension == ".txt" or extension == ".wp" or extension == ".xlsx" or extension == ".pptx" or extension == ".txt":
                    folderDestination = folder_to_track + '/Documents'
                elif extension == ".exe":
                    folderDestination = folder_to_track + '/Apps'
                elif extension == ".mp3" or extension == ".wav":
                    folderDestination = folder_to_track + '/Music'
                elif extension == ".py" or extension == ".java" or extension == ".cs":
                    folderDestination = folder_to_track + '/Coding Files'
                elif extension == ".zip":
                    folderDestination = folder_to_track + '/Zips'
                elif len(extension) > 0 and filename != "FileHandler.yaml" and filename != "FileSorter1.1.py" and filename != "FileSorter1.1.exe":
                    folderDestination = folder_to_track + '/Other'
                else:
                    skip = True
                
            if skip == False:
                time.sleep(0.1)
                src = folder_to_track + "/" + filename
                newDestination = folderDestination + "/" + filename

            
                try:
                    os.rename(src, newDestination)
                    return filename
                except OSError as error:
                    if "[WinError 3] The system cannot find the path specified:" in str(error):
                        print("\nYour Downloads folder does not contain a necessary folder.")
                        print("...")
                        os.mkdir(folderDestination)
                        print("The folder has been created for you.")
                    if first == True:
                        first = False


f = open("folder_info.txt", 'a')
f.close()

file_info = open("folder_info.txt", "r", encoding="UTF8")

info = file_info.readlines()
file_info.close()


if len(info) < 1:
    print("You need to have the following folders in your Downloads folder: \n"
          "Images \n"
          "Videos \n"
          "Documents \n"
          "Apps \n"
          "Music \n"
          "Coding Files \n"
          "Zips \n"
          "Others \n"
          "\n")
    folder_to_track = input("Enter the location of your downloads folder (e.g. C:/Users/Name/Downloads): ")
else:
    folder_to_track = info[0].strip()

folder_found = False

file_info = open("folder_info.txt", "w", encoding="UTF8")

while folder_found == False:
    if os.path.exists(folder_to_track) == True:
        file_info.write(folder_to_track)
        folder_found = True
    else:
        print("\n The folder was not found.")
        folder_to_track = input("Enter the location of your downloads folder (e.g. C:/Users/Name/Downloads): ")
        print("\n The information has been saved.")

file_info.close()

print("\n[ Running... ]")
first = True
x = 1
eventHandler = MyHandler()
observer = Observer()
observer.schedule(eventHandler, folder_to_track, recursive=True)
observer.start()

try:
    while True:
        time.sleep(10)

except KeyboardInterrupt:
    observer.stop()

observer.join()