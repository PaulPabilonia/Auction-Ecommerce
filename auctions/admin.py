from django.contrib import admin
from .models import AuctionList, Bid, Comments, User

# Register your models here.
admin.site.register(User)
admin.site.register(Bid)
admin.site.register(AuctionList)
admin.site.register(Comments)