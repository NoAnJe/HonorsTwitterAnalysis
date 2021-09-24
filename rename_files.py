import os

os.chdir("Data")

for file in os.listdir("."):
    if 'Z' in file:
        new_filename = file.replace('Z', '')
        os.rename(file, new_filename)