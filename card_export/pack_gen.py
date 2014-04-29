import random

import card_export.utils as utils


class Pack():
    def __init__(self):
        self.commons   = []
        self.uncommons = []
        self.rare      = ""
        self.foil      = ""
    
    def gen_pack(self, set):    
        commons     = utils.get_cards_by_rarity(set, 'Common')
        uncommons   = utils.get_cards_by_rarity(set, 'Uncommon')
        rares       = utils.get_cards_by_rarity(set, 'Rare')
        mythics     = utils.get_cards_by_rarity(set, 'Mythic Rare')
        basic_lands = utils.get_cards_by_rarity(set, 'Basic Land')
        
        all         = commons + uncommons + rares + mythics
                     
        foil_flag   = random.randint(1,4)
        mythic_flag = random.randint(1,8)
        
        if(foil_flag == 4):
            self.commons = random.sample(commons, 9)
            self.foil    = random.sample(all, 1)
        else:
            self.commons   = random.sample(commons, 10)  
              
        self.uncommons = random.sample(uncommons, 3)
        
        if(mythic_flag == 8):
            self.rare = random.sample(mythics, 1)
        else:
            self.rare = random.sample(rares, 1)
        

# set = 'Born of the Gods'
#  
#    
#  
#  
#  
# pack = Pack()
# pack.gen_pack(set)
#  
# print(pack.commons)
# print(pack.uncommons)
# print(pack.rare)
# print(pack.foil)





   
        
        
        