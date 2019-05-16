from newspaper import Article, ArticleException, Config
from pathlib import Path
import os, traceback, sys, string, re, urllib, urllib.request
from folderPaths import Folders
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class MyHTTP(urllib.request.HTTPHandler):
    def http_request(self, req):
        req.headers['User-agent'] = "Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11"
        return super().http_request(req)


class MediaDownloader:
    reservedChars = {';', '@', '+', ',','`'}
    escapedChars = {';': '%3B', '/': '%2F', '?': '%3F', ':': '%3A', '@': '%40', '&': '%26', '=': '%3D', '+' : '%2B', '$': '%24', ',': '%2C', '`': '%60'}

    def initGoogle(self):
        driver = webdriver.Chrome(
            'D:/ChromeDriver/chromedriver')  # Optional argument, if not specified will search path.
        driver.get('http://www.google.com/xhtml');
        time.sleep(2)  # Let the user actually see something!
        return driver

    def downloadImage(self,img_url, filename):
        #imgfilename =  imgurl.split('/')[-1]
        #imgPath = Path(imgfolder)
        #with open(imgfilename, 'wb') as f:
            #f.write(self.readImage(imgurl))
        try:
            print("downoading image  %s  to file %s" % (img_url, filename))
            opener = urllib.request.build_opener(MyHTTP())
            urllib.request.install_opener(opener)
            fname,headers = urllib.request.urlretrieve(img_url.strip(), filename)
            #print (headers)
        except Exception as e1:
            print("Exception in dowloadImage(): image_url: %s, fname : %s, Error %s " % (img_url,filename, e1))

    def download_image(self, img_url, filename):
        try:
            image_on_web = urllib.urlopen(img_url)
            if image_on_web.headers.maintype == 'image':
                buf = image_on_web.read()
                with open(filename, 'wb') as downloaded_image:
                    downloaded_image.write(buf)
                image_on_web.close()
            else:
                return False
        except:
            return False
        return True

    def readImage(self,url):
        import urllib.request
        with urllib.request.urlopen(url) as response:
            return response.read()

    '''
        Reads and Parses the match Results File
    '''
    def readMatchedFile(self,file, dir):
        with open(Path(dir) / file, 'r', encoding="utf-8") as reader:
            newslist = reader.readlines()
        # dateset Filename is the 3rd Column in first line of matched file
        datasetfile_name = newslist[0].split('|')[2]
        return newslist,datasetfile_name

    def downloadImages(self,imgs, dir, fname_pattern):
        i = 1
        for imgurl in imgs:
            try:
                im_url = imgurl.strip()
                imgfilename = im_url.split('/')[-1].strip()
                ext = Path(imgfilename).suffix.strip()
                # remove any trailing url portions with '?' '&' '%'
                ext = ext.split('?')[0].strip().split('&')[0].strip().split('%')[0].strip()
                imgfname = str(Path(dir) / (Path(fname_pattern).stem + '_' + str(i)))
                imgfname = imgfname.replace('.','_') + ext
                if not Path(imgfname).is_file():
                    self.downloadImage(img_url=im_url, filename=imgfname)
            except Exception as e1:
                print("Exception in dowloadImages(): image_url: %s : %s" % (im_url ,e1))
            i += 1


if __name__ == '__main__':
    '''
        Run this program by providing a folder containing Google Search Results.
        It reads teh corresponding dataset file contents and tries to match dataset contents with google result article text.
        It does the required cleaning of content to facilitate the matching
    '''
    # Set the directory you want to start from
    paths = Folders(rootDir='D:/Data/FakeNews/fakeNewsDatasets/', inputDir='fakeNewsDataset/legit')
    google_Root = paths.getGoogleResultsRoot()
    #***************   prepare output folders ***********************************
    matches_out = paths.getMatchesRoot()
    content_out = paths.getContentRoot()
    image_out = paths.getImagesRoot()
    #********  used for re-starts of the job, to indicate the start file name in google_Root to start processing ****
    #*******  file before start file are ignored
    start_file = None
    #**********************************************************
    files = [f for f in os.listdir(matches_out) if os.path.isfile(os.path.join(matches_out,f))]
    print(files)
    processAll = False
    count = 0
    d = MediaDownloader()
    for f in files:
        if (processAll or (start_file is None) or (start_file is not None and f == start_file)):
            processAll = True
        else:
            continue
        #***** read corresponding dataset file content
        # ***** strip all newlines and punctuation chars
        matchfile_data, dataset_file = d.readMatchedFile(f, dir=matches_out)
        #*********************************************
        match_metadata = matchfile_data[0].split('|')
        # url is the 6th Column in the match_metadata
        url = match_metadata[5].strip()
        print(url)
        imgs = []
        try:
            # image metadat is teh second line
            img_data = matchfile_data[1].split('|')
            # image urls are the 4th Column of the image metadata
            if (img_data[3]):
                imgs = img_data[3].split(',')
            c = Config()
            c.request_timeout = 15
            article = Article(url,c)
            article.download()
            article.parse()
            text = article.text
            out_file = content_out / dataset_file
            if not Path(out_file).is_file():
                with open(out_file, 'w', encoding="utf-8") as writer:
                    writer.write(article.text)
        except Exception as e:
            print(e)
        d.downloadImages(imgs=imgs, dir=image_out, fname_pattern=dataset_file)
        print(" Total images in %s is %s " % (dataset_file, len(imgs)))
        print(" Size of content in %s is %s " % (dataset_file, len(article.text)))
