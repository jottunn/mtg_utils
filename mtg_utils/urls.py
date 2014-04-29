from django.conf.urls import patterns, include, url
# from coffin.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings



from mtg_utils import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mtg_utils.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^pack-viewer/', include('pack_viewer.urls', namespace="pack_viewer")),
    url(r'^stats-viewer/', include('stats_viewer.urls', namespace="stats_viewer")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'mtg_utils.views.index', name='home' )
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
