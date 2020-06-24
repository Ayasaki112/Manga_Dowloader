import requests
import urllib.request
from urllib.request import urlopen, Request
import os
import sys
import re
from bs4 import BeautifulSoup

class AppURLopener(urllib.request.FancyURLopener):
    version='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'

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
    
def download_manga(url,remaining):
    #name of the website 
    website = 'Mangazuki_Site'
    
    if remaining==0:
        return
    
    # title and chapter
    page = get_page(url)
    title = page.find('div',{'class':'main-col col-md-12 col-sm-12 sidebar-hidden'})
    title = str(title.find('h1').text)
    x = title.find('Chapter')
    chapter = title[x:]
    title = title.replace(chapter,"")
    title = re.sub('[\W_]+', '', title)
    chapter = re.sub('[\W_]+', '', chapter)
    print(" Title : ",title)
    print(" Chapter : ",chapter)
    #image links
    content = page.find('div',{'class':'reading-content'})
    imgs = content.find_all('img')
    links = []
    for img in imgs:
        link =str(img['src'])
        link = link.replace(" ","")
        link = link.replace("\t","")
        link = link.replace("\n","")
        links.append(link)
        print(link)
    
    #make folders and subfolders
    makemydir(website)
    title = title.replace(" ","_")
    makemydir(title)
    chapter = chapter.replace(" ","_")
    makemydir(chapter)
    
    #make the html for offline viewing and save the images
    f = open(chapter+".html", "w")
    f.write("")
    f.close()
    f = open(chapter+".html", "a")
    f.write("<!DOCTYPE html>\n<html>\n<body>\n")
    loc_img_count=0
    total = len(links) 
    print(links)
    for link in links:
        if 'https' in link:
            loc_img_count+=1
            b = "  Downloading image "+str(loc_img_count)+" out of "+str(total)+" "
            sys.stdout.write('\r'+b)
            resource = opener.open(str(link))
            if resource.code == 403:
                print("\n\n Error 403 : File unreadable, saving an online copy with the manga pages \n\n")
                f.write("<img src=\""+link+"\" style=\"width:100%;height:100%;\" alt=\"\" />\n")
                continue
            filename = chapter + "img" + str(loc_img_count) + ".jpg"
            output = open(filename,"wb")
            output.write(resource.read())
            output.close()
            f.write("<img src=\""+filename+"\" style=\"width:100%;height:100%;\" alt=\"\" />\n")
    f.write("</body>\n</html>")
    f.close()
    if remaining>1:
        next_chapter = page.find('div',{'class':'nav-links'})
        next_chapter = next_chapter.find('a',{'class':'btn next_page'})['href']
        next_chapter = str(next_chapter)
        print(next_chapter)
        next_chapter = next_chapter.replace(" ","")
    os.chdir('..')
    os.chdir('..')
    os.chdir('..')
    if remaining>1:
        download_manga(next_chapter,remaining-1)

#download_manga('https://mangazuki.site/comic/hero-i-quit-a-long-time-ago/chapter-190/',5)
#inp1 = input(' Enter the url : ')
#inp3 = int(input(' Enter the total number of chapters to be downloaded,starting from the chapter in the link : '))
#download_manga(inp1,inp3)