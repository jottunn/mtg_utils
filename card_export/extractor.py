import urllib.request as req
# import xml.etree.ElementTree as ET
import codecs
    
import lxml.etree as ET
import lxml.html as HTML
import lxml.builder as E


from utils import get_card, store_cards
            


if(__name__ =="__main__"):
    for card in range(380364, 380529):
        get_card(card)
        print("card: " + str(card) + " scraped.")


