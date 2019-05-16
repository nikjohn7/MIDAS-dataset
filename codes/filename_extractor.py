import os, csv

f=open("C:/Data/FakeNews/fakeNewsDatasets/data.csv",'r+')
w=csv.writer(f)
for path, dirs, files in os.walk("C:/Data/FakeNews/fakeNewsDatasets/fakeNewsDataset/legit"):
    for filename in files:
        filename=filename[:-4]
        w.writerow([filename])