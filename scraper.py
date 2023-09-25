# web scraping imports
import requests
from bs4 import BeautifulSoup

# this function returns html text
def getdata(url):
    r = requests.get(url)
    return r.text

htmldata = getdata("https://www.pokencyclopedia.info/en/index.php?id=sprites/gen5/spr_black-white")
soup = BeautifulSoup(htmldata, 'html.parser')

read = False
stall = 0
index = 1

pokeData = {}
prevName = "pokemon-name"
# web scrap names of the pokemon
for item in soup.find_all('a'):
    # create pokemon objects. each object will contain: name, number, image

    # Reads pokemon from bulbasaur to genesect (only reads the pokemon names)
    if(item.get_text() == "Bulbasaur"):
        read = True
    
    # rotom and kyurem are the only pokemon that have adjectives before their actual pokemon name, deal with them on a case by case basis
    if(read and item.get_text() == "rotom"):
        pokeData["pokemon" + str(index)] = {'name': item.get_text(), 'number': index, 'image': "placeholder"}
        # stall = (number of extra forms) + 1 (include the original form)
        stall = 5
        index+=1
    elif(read and item.get_text() == "kyurem"):
        pokeData["pokemon" + str(index)] = {'name': item.get_text(), 'number': index, 'image': "placeholder"}
        stall = 3
        index+=1
    # this if statement avoids reading the same pokemon with multiple forms (E.g. deerling's spring form)
    # the code works when there are no adjectives before the pokemon's name
    # must check if the pokemon name has the previous name AND a space. Or else pokemon like paras and parasect will fulfill just the "contains paras" condition so this space is necessary!!!
    if(read and stall == 0 and not((prevName in item.get_text()) and " " in item.get_text())):
        # make the name of the pokemon only word, remove all following adjectives
        if(" " in item.get_text()):
            pokeData["pokemon" + str(index)] = {'name': item.get_text().split(" ", 1)[0], 'number': index, 'image': "placeholder"}
        else:
            pokeData["pokemon" + str(index)] = {'name': item.get_text(), 'number': index, 'image': "placeholder"}
        index+=1
        # splits the text using spaces as separate and takes index 0 (the first word)
        prevName = item.get_text().split(" ", 1)[0]
        # print(prevName)
    if(item.get_text() == "Genesect"):
        read = False
    if(stall > 0):
        stall-=1

for item in soup.find_all('img'):
    # item['src'] returns excess ".." at the front of the string and we need to put "https://www.pokencyclopedia.info/" before the string to get the proper src
    item['src'] = "https://www.pokencyclopedia.info/" + item['src'][2:]

    # start counting the index when you find bulbasaur's sprite (and not other random image files on the website)
    if(str(item['src']) == "https://www.pokencyclopedia.info//sprites/gen5/spr_black-white/spr_bw_001.png"):
        index = 1
    
    # the reason why the if statements look so strict is because if the link does not follow this exact format, the database WILL HAVE DUPLICATES of pokemon with multiple forms!!! Very important
    # TODO find another solution later
    if(index < 10):
        # used to remove the excess images (E.g. the website logo, other unnecessary images that are not pokemon 2d sprites)
        if(("https://www.pokencyclopedia.info//sprites/gen5/spr_black-white/spr_bw_00"+str(index)+".png" == str(item['src'])) or
        ("https://www.pokencyclopedia.info//sprites/gen5/spr_black-white/spr_bw_00"+str(index)+"_f.png" == str(item['src']))):
            pokeData["pokemon" + str(index)]['image'] = item['src']
            index+=1
    elif(index < 100):
        # used to remove the excess images (E.g. the website logo, other unnecessary images that are not pokemon 2d sprites)
        if(("https://www.pokencyclopedia.info//sprites/gen5/spr_black-white/spr_bw_0"+str(index)+".png" == str(item['src'])) or
        ("https://www.pokencyclopedia.info//sprites/gen5/spr_black-white/spr_bw_0"+str(index)+"_f.png" == str(item['src']))):
            pokeData["pokemon" + str(index)]['image'] = item['src']
            index+=1
    elif(("https://www.pokencyclopedia.info//sprites/gen5/spr_black-white/spr_bw_0"+str(index)+".png" == str(item['src'])) or
        ("https://www.pokencyclopedia.info//sprites/gen5/spr_black-white/spr_bw_0"+str(index)+"_f.png" == str(item['src']))):
        pokeData["pokemon" + str(index)]['image'] = item['src']
        index+=1

# I CANNOT PRINT ALL ITEMS IN THIS OBJECT, its okay, we do not need to.
# print(pokeData)

# install pyrebase4 so it does not conflict with requests class
import pyrebase
# keep the database information in another file for security
from configObj import config

# THIS IS PERSONAL PROJECT INFORMATION, DO NOT SHOW TO PROTECT DATA!!!

firebase = pyrebase.initialize_app(config)
database = firebase.database()

# YOU MUST GO TO THE RULES AND CHANGE "WRITE" TO "TRUE" IN ORDER TO WRITE TO THE DATABASE!!!!

# push data
database.push(pokeData)