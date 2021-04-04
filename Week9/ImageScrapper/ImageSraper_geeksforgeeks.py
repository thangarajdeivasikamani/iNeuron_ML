import requests
from bs4 import BeautifulSoup


def getdata(url):
    r = requests.get(url)
    if r.status_code == 200:
       return r.text
    else:
        return ("unable to open the page")


htmldata = getdata("https://www.geeksforgeeks.org/")
soup = BeautifulSoup(htmldata, 'html.parser')
for item in soup.find_all('img'):
    print(item['src'])