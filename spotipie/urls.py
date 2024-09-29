from django.urls import path
from .views import base_views, search_views, track_views


app_name = 'spotipie'

urlpatterns = ([
    # base_views.py
    path('', base_views.index, name='index'),
    path('callback/', base_views.callback, name='callback'),

    # search_views.py
    path('search/', search_views.search, name='search'),

    # track_views.py
    path('track/<str:track_id>/', track_views.play_track, name='play_track'),
    path('my_library/', track_views.my_library, name='my_library'),
    path('my_library/delete/<str:track_uri>/', track_views.delete_track, name='delete_track'),
])
