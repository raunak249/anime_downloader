import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

PRIMARY_URL = "http://www.gogoanime.tv"
SEARCH_URL = "/search.html?keyword="
#INFO_API = PRIMARY_URL + '/ajax/episode/info'
mozhdr = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}
serial = []
name = []
link = []


def anime_search(anime_name):
    count = 0
    url = PRIMARY_URL + SEARCH_URL + anime_name
    page_get = requests.get(url, headers = mozhdr)
    soupdata = BeautifulSoup(page_get.text,"lxml")
    allDivs = soupdata.findAll("div", attrs = {'class' : 'img' })
    for x in allDivs:
        link_current = PRIMARY_URL + x.find('a')['href']
        title = x.find('a')['title']
        serial.append(count)
        name.append(title)
        link.append(link_current)
        print(str(count + 1)+". Anime Name : " + name[count])
        count += 1
        print("-------------------------------------------")

        '''if(x.get("data-jtitle") and x.get("data-jtitle")):
            serial.append(count)
            name.append(x.get("data-jtitle"))
            link.append(x.get("href"))
            print(str(count + 1)+". Anime Name : " + name[count])
            count += 1
            print("-------------------------------------------")'''

    anime_choice = int(input("Which one from the list would you like to download?(Enter it's corresponding number \n"))
    print(name[anime_choice-1] + " is selected.")
    download_choice(anime_choice-1)


def download_single(anime_choice):
    #print(link[anime_choice])
    ep_no = int(input("Enter the episode number that you want to download \n"))
    anime_name = link[anime_choice].split('/')[-1]
    #print(anime_name)
    mod_link = PRIMARY_URL + '/' + anime_name + '-episode-' + str(ep_no)
    #print(mod_link)
    page_get = requests.get(mod_link, headers = mozhdr)
    soupdata = BeautifulSoup(page_get.text, "lxml")
    allDivs = soupdata.findAll("div", attrs = {'class' : 'download-anime' })
    for x in allDivs:
        link_download_site = x.find('a')['href']
        #print(link_download_site)
    page_get = requests.get(link_download_site, headers = mozhdr)
    soupdata = BeautifulSoup(page_get.text, "lxml")
    download_divs = soupdata.findAll("div", attrs = {'class':'dowload'})
    for x in download_divs:
        download_link = x.find('a')['href']
        break
    #print(download_link)
    testread = requests.head(download_link)
    filelength = int(testread.headers['Content-length'])
    r = requests.get(download_link, stream = True)
    print("Download Started")
    with open(name[anime_choice]+str(ep_no), 'wb') as f:
                pbar = tqdm(unit = "KB", total=int(filelength/1024) )
                for chunk in r.iter_content(chunk_size = 1024):
                    if chunk:
                        pbar.update()
                        f.write(chunk)
    print("Download complete \n")

def download_batch(anime_choice):
    #print("download_batch" + anime_name)
    start_ep = int(input("Enter the starting episode number that you want to download\n"))
    end_ep = int(input("Enter the ending episode number that you want to download\n"))
    anime_name = link[anime_choice].split('/')[-1]
    for ep in range(start_ep,end_ep+1):
        mod_link = PRIMARY_URL + '/' + anime_name + '-episode-' + str(ep)
        #print(mod_link)
        page_get = requests.get(mod_link, headers = mozhdr)
        soupdata = BeautifulSoup(page_get.text, "lxml")
        allDivs = soupdata.findAll("div", attrs = {'class' : 'download-anime' })
        for x in allDivs:
            link_download_site = x.find('a')['href']
            #print(link_download_site)
        page_get = requests.get(link_download_site, headers = mozhdr)
        soupdata = BeautifulSoup(page_get.text, "lxml")
        download_divs = soupdata.findAll("div", attrs = {'class':'dowload'})
        for x in download_divs:
            download_link = x.find('a')['href']
            break
        #print(download_link)
        testread = requests.head(download_link)
        filelength = int(testread.headers['Content-length'])
        r = requests.get(download_link, stream = True)
        print("Episode " + str(ep) + " Download Started")
        chunk_size = 1024
        with open(name[anime_choice]+str(ep), 'wb') as f:
                    pbar = tqdm(unit = "KB", total=int(filelength/(chunk_size)) )
                    for chunk in r.iter_content(chunk_size = chunk_size):
                        if chunk:
                            pbar.update()
                            f.write(chunk)
        print("Episode " + str(ep) + " Download Complete \n")

    print("All episodes downloaded.")




def check_input(anime_name):
    if(len(anime_name) == 0):
        anime_name = input("Oh I am sorry, I didn't get you. Can you enter the name again? \n")
        anime_name = check_input(anime_name)
    return anime_name

def download_choice(anime_choice):
    print("1. Download a single episode")
    print("2. Download a batch of episodes")
    choice = int(input("Please enter your choice as 1 or 2\n"))
    if(choice == 1):
        download_single(anime_choice)
    elif(choice == 2):
        download_batch(anime_choice)

def interface():
    print("Hey there! O genki desu ka? Welcome to Anime_Downloader ")
    anime_name = input("Please enter the name of the anime you want to download.\n")
    anime_name = check_input(anime_name)
    anime_search(anime_name)


if __name__ == '__main__':
    interface()
