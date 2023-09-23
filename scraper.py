import requests
from bs4 import BeautifulSoup

# this function returns html text
def getdata(url):
    r = requests.get(url)
    return r.text

htmldata = getdata("https://www.pokencyclopedia.info/en/index.php?id=sprites/gen5/spr_black-white")
soup = BeautifulSoup(htmldata, 'html.parser')

read = False
# web scrap names of the pokemon
for item in soup.find_all('a'):
    # Reads pokemon from bulbasaur to genesect (only reads the pokemon names)
    if(item.get_text() == "Bulbasaur"):
        read = True
    if(read):
        print(item.get_text())
    if(item.get_text() == "Genesect Chill Drive"):
        read = False

for item in soup.find_all('img'):
    # item['src'] returns excess ".." at the front of the string and we need to put "https://www.pokencyclopedia.info/" before the string to get the proper src
    item['src'] = "https://www.pokencyclopedia.info/" + item['src'][2:]
    # now we need to remove the excess images (E.g. the website logo, other unnecessary images that are not pokemon 2d sprites)
    if("sprites/gen5/spr_black-white" in item['src']):
        print(item['src'])

    # now we store items in excel file
    # we also need to extract the name

    # excel file will have:
    # column 1 - pokemon number
    # column 2 - pokemon name
    # column 3 - pokemon src