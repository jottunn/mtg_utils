from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Template, Context

from pack_viewer.models import Cards, Sets

import card_export.pack_gen as pack_gen
import card_export.utils as utils


def home(request):
    apps = {"Sealed Pool Generator": "sealed-chooser/", 
            "Pack Generator":        "pack-chooser/"}
    
    return render(request, "pack_index.html", {'apps': apps})


def pack_generator(request, url):
    if url == "pack-chooser":
        pack_nr = [1]
    elif url == "sealed-chooser":
        pack_nr = range(1,7)    
    
    packs = {}
    for pck in pack_nr:
        set_id = 'set_id' + str(pck)
        if 'set_id1' in request.GET:
            set_id = int(float(request.GET[set_id]))
         
        pack = pack_gen.Pack()
        pack.gen_pack(set_id)
        
        comm_imgs = []
        for common in pack.commons:
            img   = Cards.objects.get(pk=common)
            color = utils.get_card_color(img.cost)           
            comm_imgs.append((img.img, color))
        
        uncomm_imgs= []
        for uncommons in pack.uncommons:
            img = Cards.objects.get(pk=uncommons)
            color = utils.get_card_color(img.cost)
            uncomm_imgs.append((img.img, color)) 
          
        img = Cards.objects.get(pk=pack.rare[0])
        color = utils.get_card_color(img.cost)
        rare_img = [(img.img, color)]
        
        try:
            img = Cards.objects.get(pk=int(pack.foil[0]))
            color = utils.get_card_color(img.cost)
            foil_img = [(img.img, color)]
        except:
            foil_img = ""
            
        packs[pck] = {'commons':   comm_imgs,
                      'uncommons': uncomm_imgs,
                      'rare':      rare_img,
                      'foil':      foil_img}                

    return render(request, "pack_viewer.html", {'packs': packs})

    
def pack_chooser(request):
    sets = Sets.objects.all()
    
    return render(request, "pack_chooser.html", {'sets': sets})


def sealed_chooser(request):
    sets = Sets.objects.all()
    
    return render(request, "sealed_chooser.html", {'pack_nr': range(1,7),
                                                   'sets':    sets})    



