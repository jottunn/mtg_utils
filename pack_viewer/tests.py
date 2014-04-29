from django.test import TestCase
import re

asd = r'^pack/(?P<set_id>\d+)/$'

str = "/pack-viewer/pack/?set_id=1"

m = re.match(r'^pack/(?P<set_id>\d+)/$', str)
print(m)
