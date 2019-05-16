import os
from folderPaths import Folders
from pathlib import Path

folders = Folders(rootDir='D:\\Data\\FakeNews\\fakeNewsDatasets',inputDir='fakeNewsDataset\\legit')
print(folders.getMatchesRoot())
files = [f.strip() for f in os.listdir(folders.getMatchesRoot()) if os.path.isfile(os.path.join(folders.getMatchesRoot(),f))]
print(len(files))
contentfiles = [f.strip() for f in os.listdir(folders.getContentRoot()) if os.path.isfile(os.path.join(folders.getContentRoot(), f))]
contentfiles = set(contentfiles)
print(len(contentfiles))
count = 0
for file in files:
    if file in contentfiles:
        contentfiles.remove(file)
print(contentfiles)
print(len(contentfiles))