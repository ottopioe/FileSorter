
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

        for filename in os.listdir(folderToTrack):
            
            extension = os.path.splitext(filename)[1]
            if extension != ".part" or extension != ".crdownload":
                if extension == ".jpg" or extension == ".png" or extension == ".tiff" or extension == ".gif" or extension == ".webp":
                    folderDestination = '/Users/Otto/Downloads/Images'
                elif extension == ".mp4" or extension == ".mov" or extension == ".mpg":
                    folderDestination = '/Users/Otto/Downloads/Videos'
                elif extension == ".pdf" or extension == ".docx" or extension == ".html" or extension == ".doc" or extension == ".txt" or extension == ".wp" or extension == ".xlsx" or extension == ".pptx":
                    folderDestination = '/Users/Otto/Downloads/Documents'
                elif extension == ".exe":
                    folderDestination = '/Users/Otto/Downloads/Apps'
                elif extension == ".mp3" or extension == ".wav":
                    folderDestination = '/Users/Otto/Music'
                elif len(extension) > 0:
                    folderDestination = '/Users/Otto/Downloads/Others'
                else:
                    folderDestination = '/Users/Otto/Downloads'

            time.sleep(0.1)
            src = folderToTrack + "/" + filename
            newDestination = folderDestination + "/" + filename
            
            try:
                os.rename(src, newDestination)
            except OSError:
                if first == True:
                    print("Your file already exists!\n")
                    first = False
            

folderToTrack = '/Users/Otto/Downloads'
first = True
x = 1
eventHandler = MyHandler()
observer = Observer()
observer.schedule(eventHandler, folderToTrack, recursive=True)
observer.start()

try:
    while True:
        time.sleep(10)

except KeyboardInterrupt:
    observer.stop()

observer.join()