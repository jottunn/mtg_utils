from __future__ import unicode_literals

from django.db import models



class Cards(models.Model):
    set = models.ForeignKey('Sets', blank=True, null=True)
    set_number = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=60, blank=True)
    type = models.CharField(max_length=60, blank=True)
    rarity = models.CharField(max_length=60, blank=True)
    cost = models.CharField(max_length=60, blank=True, null=True)
    cmc = models.IntegerField(blank=True, null=True)
    power = models.CharField(max_length=60, blank=True, null=True)
    text = models.CharField(max_length=1000, blank=True, null=True)
    gatherer_id = models.IntegerField(blank=True, null=True)
    img = models.CharField(max_length=30, blank=True)
    
    class Meta:
        verbose_name_plural = "Cards"
    
    def __str__(self):              
        return self.name


class Sets(models.Model):
    name = models.CharField(max_length=60, blank=True)
    gatherer_start = models.IntegerField(blank=True, null=True)
    gatherer_stop = models.IntegerField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Sets"
      
    def __str__(self):              
        return self.name

