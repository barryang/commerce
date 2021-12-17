from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class categories(models.Model):
    name = models.CharField(max_length=64)

class auction_listings(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField()
    price = models.FloatField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner_listing")
    description = models.CharField(max_length=64)
    datetime = models.DateTimeField()
    category = models.ForeignKey(categories, on_delete=models.CASCADE, related_name="category")
    highestbidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="highestbidder", blank=True, null=True)

class bids(models.Model):
    item = models.ForeignKey(auction_listings, on_delete=models.CASCADE, related_name="object_bid")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner_bid")
    bid = models.FloatField()

class comments(models.Model):
    item = models.ForeignKey(auction_listings, on_delete=models.CASCADE, related_name="object_comment")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner_comment")
    comment = models.CharField(max_length=64)

class wishlist(models.Model):
    item = models.ForeignKey(auction_listings, on_delete=models.CASCADE, related_name="object_wishlist", related_query_name="wish")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner_wishlist")
    true = models.BooleanField()
    