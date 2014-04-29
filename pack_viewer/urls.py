from django.conf.urls import patterns, include, url
# from coffin.conf.urls.defaults import *

from pack_viewer import models, views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mtg_utils.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.home, name='home'),
#     url(r'^pack/(?P<set_id>\d+)/$', views.pack_generator, name='pack_generator'),
    url(r'^pack/(\w+-\w+)/$', views.pack_generator, name='pack_generator'),
    url(r'^pack-chooser/$', views.pack_chooser, name='pack_chooser'),
#     url(r'^(sealed-chooser)/$', views.pack_chooser, name='pack_chooser'),
    url(r'^sealed-chooser/$', views.sealed_chooser, name='sealed_chooser'),
)
