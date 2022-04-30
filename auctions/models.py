from django.conf.urls import url
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import BLANK_CHOICE_DASH
from django.db.models.query_utils import select_related_descend

#AbstractUser automatic creating model and add some fields for the User
# Ex. username, password, email, firstname,lastname and etc.
class User(AbstractUser):
    pass

class Bid(models.Model):
    #IntergerField to store numbers/intergers
    bid = models.IntegerField(default = 0)
    #ForeignKey is to address/link it to another table or model like the "User table/model"
    #the on_delete=models.CASCADE means that if the User get deleted all the link fields will also get deleted
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="bid")

    def _str_(self):
        return f"User: {self.user} Bids : {self.bid}"

class AuctionList(models.Model):
    #default = None means that it will store none if the user decides not to fill the data.
    owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name="auctionlist",default=None)
    bid = models.ForeignKey(Bid, on_delete = models.CASCADE, related_name = "auctionlist", default = None)
    item_name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    url = models.CharField(max_length=800)
    starting_price = models.IntegerField(default=0)
    category = models.CharField(max_length=20)
    #blank = true / basically it accepts even it is blank or empty it simple means it is not required
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlistings")
    #using BooleanField to know if the listings is close or not
    is_closed = models.BooleanField(default=False, null=True,blank= True)
    #auto_now_add = a start date you first add a listings
    created_at = models.DateTimeField(auto_now_add=True)
    #auto_now = the date when you modifed/update a listings
    update_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return f"{self.owner}:{self.bid}"

class Comments(models.Model):
    #commentor is basically the user that logged in it is link to the User model/table
    commentor = models.ForeignKey(User, on_delete=models.CASCADE,related_name="comments")
    #listing is the listings in auctionlist
    listings = models.ForeignKey(AuctionList, on_delete=models.CASCADE, related_name="comments")
    #text is the comments/message of the commentor/user.
    text = models.CharField(max_length=600)
    #time when the comment was add
    comment_at = models.DateTimeField(auto_now_add=True)
