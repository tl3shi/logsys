from django.conf.urls import patterns, include, url
urlpatterns = patterns('test.views',
        url(r'^(?P<test>.{0,})/$', 'test'),
                )
