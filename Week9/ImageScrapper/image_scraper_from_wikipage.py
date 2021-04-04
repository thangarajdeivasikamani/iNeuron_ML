from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import os
from urllib.request import urlopen, Request, urlretrieve
import urllib
import shutil

# Create the function to download the image,

def download_image(image):
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        target_path = './picture'
        target_folder = os.path.join(target_path, '_'.join(search_term.lower().split(' ')))
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        f = open(os.path.join(target_folder,".jpg"), 'wb')
        f.write(image_content)
        f.close()
        print(f"SUCCESS - saved {url} - as {target_folder}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")

#Sending request & find the image URL
url = "https://en.wikipedia.org/wiki/Megacity";

response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

megaTable = soup.find_all('table')[1]
imgLinkList = []


for imgLink in megaTable.find_all('a', {'class': 'image'}):
    partialLink = 'https://en.wikipedia.org/' + imgLink['href']
    ua1 = UserAgent()
    randomHeader = {'User-Agent': str(ua1.random)}
    imgPage = requests.get(partialLink, randomHeader)
    imgSoup = BeautifulSoup(imgPage.content, 'html.parser')
    fullImgDiv = imgSoup.find_all('div', {'class': 'fullImageLink'})
    fullImgLink = fullImgDiv[0].find_all('a')[0]
    fullImg = 'https:' + fullImgLink['href']
    imgLinkList.append(fullImg)
print(len(imgLinkList))
print(imgLinkList[1])
imagecount = list(range(len(imgLinkList)))
for i in imagecount:
   download_image(imgLinkList[i])