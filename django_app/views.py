from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect, render
from django.urls import reverse
from django.core.cache import caches
from django_app import models
from django_settings import utils
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
import re


def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    elif request.method == "POST":
        username = str(request.POST["username"])
        password = str(request.POST["password"])
        password_accept = str(request.POST["password_accept"])
        if password != password_accept:
            return render(request, "register.html", context={"error": "Пароли не совпадают!"})
        usr = User.objects.create(username=username, password=make_password(password))
        login(request, usr) 
        return redirect(reverse("main_page"))


def login_user(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        username = str(request.POST["username"])  
        password = str(request.POST["password"])  
        print(username)
        user = authenticate(username=username, password=password)
        print(user)
        if user is None:
            return render(request, "login.html", context={"error": "Логин или пароль не совпадают!"})
        login(request, user)
        return redirect(reverse("main_page"))

def logout_user(request):
    logout(request)
    return redirect(reverse("main_page"))


def search(request):
    if request.method == "POST":
        search_ = request.POST.get("search","")
        search_items = models.Item.objects.all().filter(title__icontains=search_)
        return render(
                            request=request,
                            template_name="items.html",
                            context={"items_":search_items}
            )


def main_page(request):
    categories = utils.get_cache(key=f"main_page{request.GET.get('page', 1)}", query= lambda:  models.CategoryItem.objects.all(), timeout=3600)  
    return render(
                        request=request,
                        template_name="main_page.html",
                        context={"categories":categories}
        )


def items(request,slug):
    categorie = models.CategoryItem.objects.get(slug=slug)
    items_ = utils.native_paginate(request, models.Item.objects.filter(category=categorie), 5)
    return render(
                        request=request,
                        template_name="items.html",
                        context={"categorie":categorie,"items_":items_}
        )


def item_detail(request,slug,pk):
    item = models.Item.objects.get(id=pk)
    comments = models.CommentItem.objects.all().filter(article = item)
    like = models.ItemLike.objects.all().filter(item=item,is_like=True).count()
    no_like = models.ItemLike.objects.all().filter(item=item,is_like=False).count()
    room_users = models.Room.objects.all().filter(id=1)
    return render(
                        request=request,
                        template_name="item_detail.html",
                        context={
                                "item":item,
                                "comments":comments,
                                "like":like,
                                "no_like":no_like,
                                "is_like":item.is_my_rating_selection(request.user),
                                "room_users":room_users
                                }
        )

def new_comment(request):
    comment = str(request.POST["new_comment"])
    article_id = request.POST["article"]
    slug = request.POST["categorie"]
    item = models.Item.objects.get(id=article_id)
    models.CommentItem.objects.create(author=request.user,article = item , text = comment)
    return redirect(reverse("item_detail",args=(slug,article_id,)))

def like_or_nolike(request,slug,item_id,is_like):
    author = request.user
    _item = models.Item.objects.get(id=int(item_id))
    _is_like = True if is_like == "1" else False
    try:
        # пытаюсь взять от этого пользователя к этому товару лайк или дизайн, если нет - ошибка
        like_obj = models.ItemLike.objects.get(author=author, item=_item)
        # если я раньше поставил лайк и сейчас снова жму лайк, то удалить запись
        if like_obj.is_like and _is_like:
            like_obj.delete()
        # если я раньше поставил дизлайк и сейчас снова жму дизлайк, то удалить запись
        elif not like_obj.is_like and not _is_like:
            like_obj.delete()
        # если я раньше поставил не тоже, что и сейчас, то обновляю запись
        else:
            like_obj.is_like = _is_like
            like_obj.save()
    except Exception as _:
        # создаю запись, если такой записи нет
        like_obj = models.ItemLike.objects.create(author=author, item=_item, is_like=_is_like)

    return redirect(reverse("item_detail", args=(slug,item_id,)))


def rating(request):
    _items = models.Item.objects.filter(is_active=True)
    sort = request.GET.get('sort',"desc")
    match sort:
        case "asc":
            _items = sorted(_items, key=lambda x: (x.total_rating(), x.title), reverse=False)
        case "desc":
            _items = sorted(_items, key=lambda x: (x.total_rating(), x.title), reverse=True)
        case _:
            _items = sorted(_items, key=lambda x: (x.total_rating(), x.title), reverse=True)
    return render(
                        request=request,
                        template_name="rating.html",
                        context={"items":_items,"sort":sort}
        )

def rooms(request):
    user = request.user
    _rooms = models.Room.objects.filter(users=user)
    print(_rooms)
    return render(
                        request=request,
                        template_name="rooms.html",
                        context={"rooms":_rooms}
        )

def room(request,item_author_id):
    now_user = request.user
    try:
        _room = models.Room.objects.filter(users=now_user).filter(users=item_author_id).first()
        return chat(request,_room.slug)
    except Exception:
        _room = models.Room.objects.create(
            name = 'userchat',
        )
        _room.slug = f'userchat{_room.id}'
        _room.users.add(item_author_id,now_user)
        _room.save()
        print(_room.users)
        return chat(request,_room.slug)

def chat(request,room_slug):
    _room = models.Room.objects.get(slug=room_slug)
    _messages = models.Message.objects.filter(room=_room)[:30][::-1]
    return render(request, "chat.html", context={"room": _room, "messages": _messages})