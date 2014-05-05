import psycopg2

import urllib.request as req

import codecs

import lxml.etree as ET
import lxml.html as HTML
import lxml.builder as E

import card_export.settings as settings


def connect_to_db():
    con_str = "dbname='%s' user='%s' host='%s' password='%s'" %(settings.db, settings.user, settings.host, settings.password)
    conn   = psycopg2.connect(con_str)
    cursor = conn.cursor()
    
    return cursor


class Request_obj:
    def __init__(self):
        self.url     = "http://gatherer.wizards.com/"
        
    def get_details(self, card_id):
            card_details = "Pages/Card/Details.aspx?multiverseid=%d" %card_id
            details_url  =  self.url + card_details
            
            card_img = "Handlers/Image.ashx?multiverseid=%d" %card_id + "&type=card"          
            img_url  =  self.url + card_img
                   
            return details_url, img_url
        

#scrape gatherer for cards
class My_Card:
    def __init__(self):
        self.name      = ""
        self.mana      = ""
        self.cmc       = ""
        self.type      = ""
        self.text      = ""  
        self.pt        = ""
        self.rarity    = ""
        self.set       = ""
        self.number    = ""
          


def get_card(card_id):   
    card =  Request_obj()

    detail_url, img_url = card.get_details(card_id)
    
    parser = HTML.HTMLParser(recover=True)
    tree   = HTML.parse(detail_url, parser=parser)  
    
    attributes = ["name", "mana", "cmc", "type", "text", "pt", "set", "rarity", "number"]
    carte = My_Card();
    
    for attribute in attributes:
        div   = tree.find(".//div[@id='ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_%s"%(attribute)+"Row']") 
        try:
            field = HTML.fromstring(ET.tostring(div))
        except:
            pass    
            
        if(attribute == "mana"):
            inner = HTML.fromstring(ET.tostring(field.find(".//div[@class='value']")))
            
            mana = inner.findall(".//img[@alt]")
            mana_string = ""
            
            for type in mana:
                mana_string += type.attrib['alt'] + " "
            
            setattr(carte, attribute, mana_string)
            continue
        elif(attribute == "text"):
            inner = field.findall(".//div[@class='cardtextbox']")
            card_text = ""
            
            for part in inner:
                test = part.findall(".//img[@alt]")
                
                for elem in test:
                    card_text += elem.attrib['alt']
                    try:
                        card_text += elem.tail
                    except:
                        pass                      
                try:
                    card_text += part.text
                except:
                    pass
                card_text += "\n"
                
            card_text = card_text.rstrip("\n")           
            setattr(carte, attribute, card_text)  
            continue
        elif(attribute == "set"):
            set = field.findall(".//a[@href][2]")[0]
            setattr(carte, attribute, set.text)
            continue
        elif(attribute =="rarity"):
            rarity = field.findall(".//span[@class]")[0]
            setattr(carte, attribute, rarity.text)
            continue
        
        setattr(carte, attribute, field.find(".//div[@class='value']").text.strip())        
        
    
    attrs     = vars(carte)
    details   = codecs.open("cards/card_" + str(card_id) +".card", "w", encoding = "utf-8")

    xml = ET.Element("card")
    
    for k, v in attrs.items():
        tag    = ET.SubElement(xml, k)
        tag.text = v
    
    img_tag      = ET.SubElement(xml, "img")
    img_tag.text = "img_" + str(card_id) +".jpg"
    img = open("images/" + img_tag.text, "wb")
   
    try:
        response = req.urlopen(img_url)
        img.write(response.read())
        img.close()
    except:
        img.write("N/A")
        img.close()
        
                    
    details.write(str(ET.tostring(xml, pretty_print=True).decode())) 
    details.close()

#get set range
def get_range(set_id):
    range = connect_to_db()
    
    sql         = """SELECT gatherer_start, gatherer_stop FROM pack_viewer_sets WHERE id='%d'""" %(set_id)
    range.execute(sql)
    
    data   = range.fetchall()
    (start_fetch, stop_fetch) = (data[0][0], data[0][1])
    
    range.close()
    
    return (start_fetch, stop_fetch)

 
#get cards for set byr arity
def get_cards_by_rarity(set_id, rarity):
    cards = connect_to_db()
    sql = """SELECT id FROM pack_viewer_cards 
                WHERE set_id = '%d'
                AND rarity = '%s'""" %(set_id, rarity)
    
    cards.execute(sql)
    data = cards.fetchall()
    cards.close()
    
    return [i[0] for i in data]


#calculate color
def get_card_color(cost):
    import re
    
#     card = connect_to_db()
#     sql  = """SELECT cost FROM pack_viewer_cards
#                 WHERE id = '%d'""" %(card_id)
#                 
#     card.execute(sql)
#     cost = card.fetchone()[0]
#     card.close()
    if cost is None:
        clr = "land"
        return clr    
        
    white     = re.compile('White')
    blue      = re.compile('Blue')
    red       = re.compile('Red')
    black     = re.compile('Black')
    green     = re.compile('Green')
    colorless = re.compile('\d+|Variable Colorless')
      
    colors = {white:     'white', 
              blue:      'blue', 
              red:       'red', 
              black:     'black', 
              green:     'green', 
              colorless: 'colorless'}
    
    color_cnt = 0
    
    for color, color_name in colors.items():            
        if color.search(cost):
            color_cnt += 1
            mono_color = color_name
            print(mono_color) 
                  
    if (color_cnt > 1 and not colorless.search(cost)) or (color_cnt > 2):
        clr = "multicolor"
    elif color_cnt == 1 and  colorless.search(cost):
        clr = "colorless"
    elif (color_cnt == 1 and  not colorless.search(cost)) or (color_cnt == 2 and colorless.search(cost)):
        clr = mono_color
        
    else:
        clr = "color not calculated"
                
    return clr           
            
        
#store cards in db
def store_cards(set_id):   
    set_details = connect_to_db()
    sql = """SELECT id FROM pack_viewer_sets where name='%s'""" %(set_id)
    set_details.execute(sql)
    data =  set_details.fetchall()
    
    set_details.close()
    
    start_fetch, stop_fetch = get_range(set_id)
    
    insert_cards = connect_to_db()
    
    for card_id in range(int(start_fetch), int(stop_fetch+1)):
        tree = ET.parse("cards/card_" + str(card_id) + ".card")
        card = tree.getroot()
        card_data = {}
        
        for atribute in card:
            if(atribute.tag == "cmc"):
                try: 
                    check_int = int(atribute.text)
                    card_data[atribute.tag] = str(check_int)               
                except ValueError:
                    card_data[atribute.tag] = str(0)        
            elif(atribute.tag == "pt"):
                if(atribute.text is not None):
                    p_t = atribute.text.split("/")
                    try:
                        card_data["power"]     = str(p_t[0])
                        card_data["toughness"] = str(p_t[1])
                    except:
                        card_data["power"]     = str(p_t[0])
            elif(atribute.tag == "set"):
                card_data["set_id"] = str(set_id)
            elif(atribute.tag =="mana"):
                if(atribute.text is not None):
                    card_data["cost"] = atribute.text
            elif(atribute.tag =="number"):
                card_data["set_number"] = atribute.text   
            else:
                try:
                    card_data[atribute.tag] = str(atribute.text.replace("""'""", """''"""))
                except:
                    pass
            card_data["gatherer_id"] = str(card_id)
        
        insert_cards = connect_to_db()
        
        columns = ", ".join(list(card_data.keys()))
        values  = ", ".join("'" + item + "'" for item in list(card_data.values()))
             
             
        sql = """INSERT INTO pack_viewer_cards (%s) VALUES(%s)"""%(columns, values)
        sql = sql.encode('utf_8')
        insert_cards.execute(sql)
        insert_cards.execute("COMMIT")
        
    insert_cards.close()
       


