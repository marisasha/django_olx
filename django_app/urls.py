from django.contrib import admin
from django.urls import include, path
from django_app import views,views_a

urlpatterns = [
    path('login_user',views.login_user,name = 'login_user'),
    path('logout_user',views.logout_user,name = 'logout_user'),
    path('register',views.register,name = 'register'),

    path('items/search/',views.search,name = 'search'),
    path('new_comment',views.new_comment,name = 'new_comment'),
    path('items/<str:slug>/<int:item_id>/<str:is_like>', views.like_or_nolike, name='like_or_nolike'),

    path('',views.main_page,name = 'main_page'),
    path('rating',views.rating,name='rating'),
    path('rooms',views.rooms,name='rooms'),
    path('items/<str:slug>',views.items,name='items'),
    path('items/<str:slug>/<str:pk>',views.item_detail,name='item_detail'),
    path('room/<str:item_author_id>',views.room,name='room'),
    path("chat/<slug:room_slug>/", views.chat, name="chat"),
    
]

websocket_urlpatterns = [path("ws/chat/<slug:room_name>/", views_a.ChatConsumer.as_asgi())]
