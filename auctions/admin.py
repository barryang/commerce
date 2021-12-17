from django.contrib import admin

from .models import categories, auction_listings, bids, comments, wishlist
# Register your models here.
admin.site.register(categories)
admin.site.register(auction_listings)
admin.site.register(bids)
admin.site.register(comments)
admin.site.register(wishlist)