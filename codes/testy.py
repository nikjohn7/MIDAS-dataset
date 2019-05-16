import os
import pprint
from pathlib import Path
from folderPaths import Folders
from PIL import Image  # uses pillow

class ImageData:
    def __repr__(self):
        return self.filename+':'+str(self.size) + ':' + str(self.dimensions)

    filename = ''
    filePrefix =''
    size = 0
    extension = ''
    dimensions = ()

def copyDict():
    for element in copy:
        temp = []
        filter = {}
        dkeys = copy[element]
        for i in dkeys:
            i = str(i)
            endsize = i.find(':')
            fname = i[:endsize]
            i = i[endsize + 1:]
            filter[i] = fname
            temp.append(i)
        copy[element] = temp
        temp.sort(reverse=True)
        max = temp[0]


pp = pprint.PrettyPrinter(indent=4)
paths = Folders(rootDir='C:/Data/FakeNews/fakeNewsDatasets', inputDir='fakeNewsDataset/legit')
img = paths.getImagesRoot()
imglist=os.listdir(img)
l = []
dict = {}
count = 0
removed = []
for f in imglist:
    fullpath=os.path.join(img,f)
   # print(fullpath)
    start = f.find('_')
    if start >= 0:
        fileprefix = f[:start]
        i_data = ImageData()
        i_data.filename = f
        i_data.filePrefix = fileprefix
        i_data.size = os.stat(fullpath).st_size
        i_data.extension = os.path.splitext(fullpath)[1]
        im = Image.open(fullpath)
        i_data.dimensions = im.size  # return value is a tuple, ex.: (1200, 800)
        x = i_data.dimensions[0]
        y = i_data.dimensions[1]
        if (x+y <= 600 or x/y > 2):
            count +=1
            removed.append(fullpath)
            continue
        l = []
        l.append(i_data)
        if fileprefix in dict:
            l = dict[fileprefix]
            l.append(i_data)
        else:
            dict[fileprefix] = l
pp.pprint(dict)
print(count)
with open(os.path.join(paths.getUnmatchedRoot(),'removed.txt'), 'w', encoding="utf-8") as writer:
    writer.writelines(removed)
for file in removed:
    os.remove(file)
print(" files deleted = " + str(len(removed)))