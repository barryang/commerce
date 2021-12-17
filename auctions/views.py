from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, auction_listings, bids, comments, categories, wishlist
from django import forms
from datetime import datetime

class bidform(forms.Form):
    bid = forms.FloatField(label="bid")

class commentform(forms.Form):
    comment = forms.CharField(max_length=64, label="comment")

class listingform(forms.Form):
    name = forms.CharField(max_length=64, label="name")
    image = forms.ImageField(label="image")
    price = forms.FloatField(label="starting price")
    description = forms.CharField(label="description")
    category = forms.CharField(label="category")

def index(request):
    return render(request, "auctions/index.html", {
        'items': auction_listings.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def category(request):
    return render(request, "auctions/categories.html", {
        'categories': categories.objects.all(),
    })

def activelistings(request):
    active = auction_listings.objects.filter(owner=request.user)
    return render(request, "auctions/activelisting.html", {
        'active': active,
    })
    

def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        'watch' : auction_listings.objects.filter(wish__true=True, wish__owner=request.user)
    })


def listing(request, listing_id):
    item = auction_listings.objects.get(id=listing_id)
    if request.method == "POST":
        form = bidform(request.POST)
        if form.is_valid():
            new_bid = bids(item=item, owner=request.user, bid=form.cleaned_data["bid"])
            new_bid.save()
            if form.cleaned_data["bid"] > item.price:
                item.highestbidder = request.user
                item.price = form.cleaned_data["bid"]
                item.save()
        form = commentform(request.POST)
        if form.is_valid():
            new_comment = comments(item=item, owner=request.user, comment=form.cleaned_data["comment"])
            new_comment.save()
    
    Comment = comments.objects.filter(item=item)
    bid_number = bids.objects.filter(item=item).count()
    wish = wishlist.objects.filter(owner=request.user, item=item)
    return render(request, "auctions/listing.html", {
        'listing': item,
        'comments': Comment,
        'bids': bid_number,
        'bidform': bidform(),
        'commentform': commentform(),
        'wishlist': wish
    })



def create(request):
    if request.method == "POST":
        form = listingform(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            now = datetime.now()
            name = form.cleaned_data["name"]
            image = form.cleaned_data["image"]
            price = form.cleaned_data["price"]
            description = form.cleaned_data["description"]
            categ = form.cleaned_data["category"]
            if not categories.objects.filter(name=categ).exists():
                newcategory = categories(name=categ)
                newcategory.save()
            categ = categories.objects.get(name=categ)
            newlisting = auction_listings(name = name, image = image, price = price, description = description, datetime = now, category = categ, owner = request.user)
            newlisting.save()
            return listing(request, newlisting.id)
        else:
            return render(request, "auctions/addlisting.html", {
            'form': listingform(),
        })
    else:
        return render(request, "auctions/addlisting.html", {
            'form': listingform(),
        })

def cat(request, categories_name):
    category = categories.objects.get(name=categories_name)
    return render(request, "auctions/activelisting.html", {
        'active': auction_listings.objects.filter(category=category)
    })