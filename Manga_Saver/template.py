import requests
import urllib.request
from urllib.request import urlopen, Request
import os
import sys
from bs4 import BeautifulSoup

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

opener = AppURLopener()

def makemydir(dir):
  try:
    os.makedirs(dir)
  except OSError:
    pass
  os.chdir(dir)

def get_page(url):
    page = BeautifulSoup(requests.get(url).text,"html.parser")
    return page
    
def download_manga(url,remaining,folder,f,img_count):
    if remaining==0:
        return
    page = get_page(url)
    #title = page.find('div',{'class':'main-col col-md-12 col-sm-12 sidebar-hidden'})
    #title = str(title.find('h1').text)
    #x = title.find('Chapter')
    #chapter = title[x:]
    #title=title.replace(chapter,"")
    #print("\n",title," ",chapter)
    #print(page)
    #soup = page.find('img',{'class':'_lazy chapter-img'})
    imgs = page.find_all('img')
    links = []
    for img in imgs:
        link =str(img['src'])
        link = link.replace(" ","")
        link = link.replace("\t","")
        link = link.replace("\n","")
        links.append(link)
    #print(" Currently downloading ",chapter)
    makemydir(website)
    title = title.replace(" ","_")
    makemydir(title)
    chapter = chapter.replace(" ","_")
    makemydir(chapter)
    loc_img_count=0
    total = len(links) 
    print(links)
    for link in links:
        if 'https' in link:
            print('\n working on '+link) 
            img_count+=1
            loc_img_count+=1
            b = "  Downloading image "+str(loc_img_count)+" out of "+str(total)+" "
            sys.stdout.write('\r'+b)
            resource = opener.open(str(link))#urllib.request.urlopen(str(link))
            filename = chapter + "img" + str(img_count) + ".jpg"
            output = open(filename,"wb")
            output.write(resource.read())
            output.close()
            f.write("<img src=\""+filename+"\" style=\"width:100%;height:100%;\" alt=\"\" />\n")
    if remaining>1:
        next_chapter = str(page.find('div',{'class':'nav-next '})['href'])
        print(next_chapter)
        return
        next_chapter = next_chapter.replace(" ","")
    os.chdir('..')
    os.chdir('..')
    os.chdir('..')
    if remaining>1:
        download_manga(next_chapter,remaining-1,folder,f.img_count)

chapter = "Tales of demons and lords"
f = open(chapter+".html", "w")
f.write("")
f.close()
f = open(chapter+".html", "a")
f.write("<!DOCTYPE html>\n<html>\n<body>\n")
inp1 = input(' Enter the url : ')
#inp2 = input(' Enter folder name (Folder you\'ll save the downloaded chapters in) : ')
inp3 = int(input(' Enter the total number of chapters to be downloaded,starting from the chapter in the link : '))
download_manga(inp1,inp3,f)
f.write("</body>\n</html>")
f.close()