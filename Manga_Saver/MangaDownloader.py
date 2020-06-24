import tkinter
import webtoons
import manganelo
import mangazuki_site
from tkinter import *

def download():
    website = str(variable.get()).replace('\n','')
    website = website.replace('\t','')
    url = str(E1.get())
    count = int(E2.get())
    print(website," ",url," ",count)
    if website == 'Webtoons':
        webtoons.download_manga(url,count)
    elif website == 'Manganelo':
        manganelo.download_manga(url,count)
    elif website == 'Mangazuki.site':
        mangazuki_site.download_manga(url,count)

root = tkinter.Tk()
L0 = Label(root, text="\n\tSeclet a website to download manga from\t\n")
L0.pack()
OPTIONS = ["\n\tManganelo\t\n","\n\tWebtoons\t\n","\n\tMangazuki.site\t\n"]
variable = StringVar(root)
variable.set(OPTIONS[0])
w = OptionMenu(root, variable, *OPTIONS)
w.pack()
L1 = Label(root, text="\n\t Link to the chapter you want to begin downloading from \t\n")
L1.pack()
E1 = Entry(root, bd =10)
E1.pack()
L2 = Label(root, text="\n\t Number of chapters to download \t\n")
L2.pack()
E2 = Entry(root, bd =10)
E2.pack()
B = Button(root, text ="Start Downloading", command = download )
B.pack()
root.mainloop()