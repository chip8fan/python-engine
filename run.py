# This script does an hour-long training loop.
import time
import os
import shutil
if os.path.isfile("model.pth") or os.path.isdir("pgn") or os.path.isdir("chunks"):
    confirm = input("Do you want to reset the model? (y/n) ")
    while confirm != "y" and confirm != "n":
        confirm = input("Do you want to reset the model? (y/n) ")
    if confirm == "y":
        if os.path.isfile("model.pth"):
            os.remove("model.pth")
        if os.path.isdir("chunks"):
            shutil.rmtree("chunks")
        if os.path.isdir("pgn"):
            shutil.rmtree("pgn")
        if os.path.isdir("chunks") == False:
            os.mkdir("chunks")
        if os.path.isdir("pgn") == False:
            os.mkdir("pgn")
start = time.time()
count = 0
while time.time()-start < 60*60:
    os.system('python3 play.py pgn')
    os.mkdir(f"chunks/{count}")
    os.system(f'python3 parser.py pgn/{count}.pgn chunks/{count}')
    os.system(f"python3 train.py chunks/{count}")
    count += 1