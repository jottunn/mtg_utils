# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Cards(models.Model):
    id = models.FloatField(primary_key=True)
    set = models.ForeignKey('Sets', blank=True, null=True)
    set_number = models.FloatField(blank=True, null=True)
    name = models.CharField(max_length=60, blank=True)
    type = models.CharField(max_length=60, blank=True)
    rarity = models.CharField(max_length=60, blank=True)
    cost = models.CharField(max_length=60, blank=True)
    cmc = models.FloatField(blank=True, null=True)
    power = models.FloatField(blank=True, null=True)
    toughness = models.FloatField(blank=True, null=True)
    text = models.CharField(max_length=1000, blank=True)
    gatherer_id = models.FloatField(blank=True, null=True)
    img = models.CharField(max_length=30, blank=True)
    class Meta:
        managed = False
        db_table = 'cards'

class Sets(models.Model):
    id = models.FloatField(primary_key=True)
    name = models.CharField(max_length=60, blank=True)
    gatherer_start = models.FloatField(blank=True, null=True)
    gatherer_stop = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'sets'

