import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import os, traceback, sys
from pathlib import Path
from folderPaths import Folders

def initGoogle():
    driver = webdriver.Chrome('C:/Program Files/chromeDriver/chromedriver')  # Optional argument, if not specified will search path.
    driver.get('http://www.google.com/xhtml');
    time.sleep(2) # Let the user actually see something!
    return driver


def googleSearch(searchQuery):
    driver = initGoogle()
    try:
        search_box = driver.find_element_by_name('q')
        driver.implicitly_wait(10)
        search_box.send_keys(searchQuery)
        search_box.submit()
        driver.implicitly_wait(30)
    except Exception as e:
        print(e)
    #Selenium hands the page source to Beautiful Soup
    results = []
    search_root = driver.find_elements_by_xpath("//div[@id='search']")[0]
    elements = search_root.find_elements_by_class_name('g')
    driver.implicitly_wait(10)
    result = []
    for el in elements:
        try:
            result_root = el.find_elements_by_class_name('r')[0]
            #print (result_root)
            a_result = result_root.find_element(By.TAG_NAME, 'a')
            #print(a_result)
            url = a_result.get_attribute("href")
            title = a_result.find_elements_by_tag_name("h3")[0].text
            print(" Result url %s title " % url, title)
            result =[]
            result.append(url)
            result.append(title)
            results.append(result)
        except IndexError as e:
            print(e)
    time.sleep(2)  # Let the user actually see something!
    driver.quit()
    return results

'''  
Run this to fire query on Google based on contents of each file in input folder and write Top 10 results to out folder
'''
# Set the directory you want to start from
paths = Folders(rootDir='D:/Data/FakeNews/fakeNewsDatasets/', inputDir='fakeNewsDataset/legit')
fakeNews_Root = paths.getDatasetFolder()
# write Top 10 Google Search results for each input file
out_folder = paths.getGoogleResultsRoot()
#********  used for re-starts of the job, to indicate the start file name in google_Root to start processing ****
#*******  file before start file are ignored
start_file = None
end_file = 'polit33.legit.txt'
input_folder = Path(fakeNews_Root)
#**********************************************************
outdir = Path(out_folder)
outdir.mkdir(parents=True, exist_ok=True)
try:
    files = [f for f in os.listdir(fakeNews_Root) if os.path.isfile(os.path.join(fakeNews_Root,f))]
    print(files)
    processAll = False
    for f in files:
        if (processAll or (start_file is None) or (start_file is not None and f == start_file)):
            processAll = True
        else:
            continue
        with open(input_folder / f,encoding="utf-8") as reader:
            filetxt = '  '.join(reader.readlines())
        # Take title and add words from content (Max 30 words Google limit) to form search query
        qstr = ' '.join(filetxt.split()[:30])
        results = googleSearch(qstr)
        time.sleep(2)
        out_file = Path(input_folder / f)
        googleResults_file = outdir / (out_file.stem + '.out')
        with open(googleResults_file, 'w', encoding="utf-8") as writer:
            for result in results:
                s = ' '.join(result)+ '\n'
                #print("Results for  file %s IS %s" % (f, s))
                writer.write(s)
        if (end_file is not None and f == end_file):
            break
except Exception as e:
  exc_type, exc_value, exc_traceback = sys.exc_info()
  traceback.print_exception(exc_type, exc_value, exc_traceback)
