from newspaper import Article, ArticleException, Config
from pathlib import Path
import os, traceback, sys, string, re, urllib
from folderPaths import Folders
from processMatchFiles import MediaDownloader
from bs4 import BeautifulSoup
import urllib


def downloadImage(img_url, filename):
    # imgfilename =  imgurl.split('/')[-1]
    # imgPath = Path(imgfolder)
    # with open(imgfilename, 'wb') as f:
    # f.write(self.readImage(imgurl))
    try:
        print("downoading image  %s  to file %s" % (img_url, filename))
        fname, headers = urllib.request.urlretrieve(img_url.strip(), filename)
        # print (headers)
    except Exception as e1:
        print("Exception in dowloadImage(): image_url: %s, fname : %s, Error %s " % (img_url, filename, e1))

def downloadImages(imgs, imageDir, fname_pattern):
    i = 1
    for imgurl in imgs:
        try:
            im_url = imgurl.strip()
            imgfilename = im_url.split('/')[-1].strip()
            ext = Path(imgfilename).suffix.strip()
            # remove any trailing url portions with '?' '&' '%'
            ext = ext.split('?')[0].strip().split('&')[0].strip().split('%')[0].strip()
            imgfname = str(Path(imageDir) / (Path(fname_pattern).stem + '_' + str(i)))
            imgfname = imgfname.replace('.', '_') + ext
            if not Path(imgfname).is_file():
                downloadImage(img_url=im_url, filename=imgfname)
        except Exception as e1:
            print("Exception in dowloadImages(): image_url: %s : %s" % (im_url, e1))
        i += 1
# use this image scraper from the location that
#you want to save scraped images to

def make_soup(url):
    html = urllib.request.urlopen(url).read()
    return BeautifulSoup(html)

def get_images(url):
    soup = make_soup(url)
    #this makes a list of bs4 element tags
    images = [img for img in soup.findAll('img')]
    print (str(len(images)) + "images found.")
    #compile our unicode list of image links
    image_links = [each.get('src') for each in images]
    return image_links
'''
    For a given Google results file, reads the corresponding Dataset file and return content 
'''
def readDatasetFile(file, dir):
    datasetdir = Path(dir)
    path_file = Path(file)
    dataset_file = datasetdir / (path_file.stem + '.txt')
    with open(dataset_file, 'r', encoding="utf-8") as reader:
        newslist = reader.readlines()[1:]
    newsstr = ' '.join(newslist)
    return newsstr, dataset_file.name

'''
Strip all newlines and punctuation chars
'''
def stripAndClean(instr):
    str = instr.strip().replace('\n', '').replace('\r', '')
    str = re.sub(r'[-,“’”.`?!\"\']+', ' ', str)
    table = str.maketrans({key: None for key in string.punctuation})
    str = str.translate(table)
    str = re.sub(r'[-,.?!]\s+', ' ', str)
    str = re.sub(r'[-,“’”.`?!\"\']+', ' ', str)
    str = re.sub(r'\s+', ' ', str)
    return str

'''
    Run this program by providing a folder containing Google Search Results.
    It reads teh corresponding dataset file contents and tries to match dataset contents with google result article text.
    It does the required cleaning of content to facilitate the matching
'''
# Set the directory you want to start from
paths = Folders(rootDir='D:/Data/FakeNews/fakeNewsDatasets/', inputDir='fakeNewsDataset/legit')
google_Root = paths.getGoogleResultsRoot()
#***************   prepare output folders ***********************************
matches_out = paths.getFolder('new_matched')
content_out = paths.getFolder('new_content')
dataset_root = paths.getDatasetFolder()
image_out = paths.getFolder('new_images')
unmatched_folder = paths.getFolder('new_unmatched')
noMatch_file = str(Path(unmatched_folder) / "Zero_Matches.txt")
#********  used for re-starts of the job, to indicate the start file name in google_Root to start processing ****
#*******  file before start file are ignored
start_file = None
end_file = None
#**********************************************************
files = [f for f in os.listdir(google_Root) if os.path.isfile(os.path.join(google_Root,f))]
print(files)
processAll = False
d = MediaDownloader()
count = 0


def prepareMatchOutput(matchIndex, url, outList):
    match_metadata = "match_metadata | %s | %s | %s | %s | %s " % (matchIndex, dataset_file, f, line_index, url)
    outList.append(match_metadata + '\n')
    imgs = get_images(url)
    top_img = ''
    #top_img = article.top_image
    imagestr = " images | %s | %s | %s | %s" % (matchIndex, url, top_img, ','.join(imgs))
    outList.append(imagestr + '\n')
    return imgs


def writeContentAndImages(content,contentFile, inputFile, url, imageDir, images):
    if not Path(contentFile).is_file():
        with open(contentFile, 'w', encoding="utf-8") as writer:
            writer.write(content)
    print("downoading images for %s : %s" % (inputFile, url))
    downloadImages(imgs=images, imageDir=imageDir, fname_pattern=inputFile)

for f in files:
    filecount = 0
    listOfMatches = []
    zero_matches = []
    if (processAll or (start_file is None) or (start_file is not None and f == start_file)):
        processAll = True
    else:
        continue
    #***** read corresponding dataset file content
    # ***** strip all newlines and punctuation chars
    dataset_content, dataset_file = readDatasetFile(f, dir=dataset_root )
    lines = []
    dataset_content = stripAndClean(dataset_content)
    #*********************************************
    try:
        with open(Path(google_Root) / f, encoding="utf-8", errors="ignore")  as reader:
            lines = reader.readlines()
    except UnicodeDecodeError as e1:
        print(e1)
    line_index = 0
    matched = False
    for line in lines:
        try:
            if not line:
                line_index += 1
                continue
            #** extract the url from google search results - the first word
            url = line.split(' ')[0].strip()
            url = urllib.parse.unquote(url)
            for ch in d.reservedChars:
                url = url.replace(ch, d.escapedChars[ch])
            print(url)
            try:
                c = Config()
                c.request_timeout = 15
                article = Article(url,config=c)
                article.download()
                article.parse()
            except ArticleException as e1:
                print (" Exception while fetch url file %s, url %s : err %s" % (dataset_file, url,str(e1)))
            google_txt = stripAndClean(article.text)
            #**** simple Python substring check
            if google_txt and dataset_content in google_txt:
                images = prepareMatchOutput(matchIndex=filecount, url=url, outList=listOfMatches)
                count += 1
                filecount += 1
                # we write content and images for only one match per dataset file
                out_file = str(Path(content_out) / dataset_file)
                if (not matched):
                    matched = True
                    writeContentAndImages(content=article.text,contentFile=out_file,inputFile=dataset_file,url=url,images=images,imageDir=image_out)
            line_index+=1
        except ArticleException as e1:
            print (" ArtException while match or download file %s, line %s : err %s" % (dataset_file, line ,str(e1)))
        except Exception as e:
            print(" Exception while match or download file %s, line %s : err %s" % (dataset_file, line, str(e)))
    if filecount == 0 :
        zero_matches.append(dataset_file + '\n')
        with open(noMatch_file, 'a', encoding="utf-8") as writer:
            writer.writelines(zero_matches)
        print(" No matches in file %s is %s " % (dataset_file, filecount))
    else:
        out_file = str(Path(matches_out) / dataset_file)
        print (" Total matches in file %s is %s  lines in file %s" % (dataset_file,filecount, len(listOfMatches)))
        with open(out_file, 'w', encoding="utf-8") as writer:
            writer.writelines(listOfMatches)
    if (end_file == f):
        break
print(" Total matches  is %s " % (count))
