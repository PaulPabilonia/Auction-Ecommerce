#for creating and logging user
from django.conf.urls import url
from django.contrib.auth import authenticate, login, logout
#intergrityerror for no ducplicate or repeated user
from django.db import IntegrityError
from django.db.models.query import RawQuerySet
#this return http response
from django.http import HttpResponse, HttpResponseRedirect
#this is use for rendering template or htmls
from django.shortcuts import render
#this is use to reverse the url path Ex. from views to url
from django.urls import reverse
#for messages alerts
from django.contrib import messages
from .models import User,Bid, AuctionList, Comments


def index(request):
    """
    AuctionList.object.filter it filter all the listings
    in the database that is active meaning the listing is still open for bidding
    is_closed = False means it is still active
    """
    active_listings = AuctionList.objects.filter(is_closed=False)
    return render(request, "auctions/index.html",{
            "active_listings": active_listings
        })

def submit_listings(request):
    if request.method == "POST":
        """
        This fuction get all the value from the input tag
        Using the name attribute in the input tag Ex. [name =item_name], category, description etc.
        """
        item_name = request.POST['item_name']
        user = request.user #this reference the object in User model
        category = request.POST['category']
        description = request.POST['description']
        url_image = request.POST['url_image']
        """
        it use the Bid model and use the bid object and
        get the value from the input tag and convert it to integer
        """
        starting_price = request.POST['bid'] #we are storing first bid to the starting price
        bid = Bid(bid=int(request.POST['bid']), user=user)#This cinvert the input to integer and stores 
                                                            #the bid to the bid model with the user
        bid.save() # we always need to save/add it first to the database for the foreignKey that link to the model
        listing = AuctionList(item_name=item_name,description=description, owner=user,
        starting_price = starting_price, bid=bid, is_closed = False, url = url_image, category = category)
        listing.save()
    
        return HttpResponseRedirect(reverse("index"))
        #the user will return to the index after they submit it otherwise
    #they will remain to the creatlist page
    return render(request, "auctions/createlist.html")

def category(request):
   if request.method == "POST":
       #chosen_category takes the value from the selector tag using its name attribute
        chosen_category = request.POST["category"]
        #This will filter all the active list becuase of the boolean object is_close
        active_listings = AuctionList.objects.filter(is_closed=False,category=chosen_category)
        
        return render(request, "auctions/index.html",{
            "active_listings": active_listings
        })

def category_all_list(request):
    if request.method == "POST":
        #chosen_category takes the value from the selector tag using its name attribute
        chosen_category = request.POST['category']
        #This will filter all the specific category closed or active list
        all_listings = AuctionList.objects.filter(category=chosen_category)

        return render(request,"auctions/all_list.html",{
            "all_listings": all_listings
        })

def display_list(request, listing_id):
    listing = AuctionList.objects.get(pk = listing_id)
    #this will get all the comments
    comments = listing.comments.all()

    if request.user == listing.owner:
        listing_owner = True
    else:
        listing_owner = False

    listing_in_user_watchlist = request.user in listing.watchlist.all()
    return render(request, "auctions/display_list.html",{
        'listing':listing,
        'listing_in_user_watchlist':listing_in_user_watchlist,
        'listing_owner': listing_owner,
        'comments':comments
    })

def add_watchlist(request, listing_id):
    user = request.user
    listing = AuctionList.objects.get(pk = listing_id)
    listing.watchlist.add(user) 

    messages.success(request,"+Watchlist added Successfully!")
    """
    adding the user to the watchlist to reference the listing
    Whenever the user is loggged in all the list(watchlist) that link to it(user)
    will display to the watchlist page.
    because watchlist is using Many to many field 
    it can have multiple user and the user can have multiple watchlist
    """
    #after adding the listing to the watchlist it will stay at the display_list page
    return HttpResponseRedirect(reverse('display_list', args=(listing_id,)))

def add_comment(request,listing_id):
    if request.method == "POST":
        #get the comment from the input text with the name attribute 'comment'
        comment = request.POST['comment']
        user = request.user #get the user
        #using the listing_id it will get the auctionlist that we want to add some comment
        listing = AuctionList.objects.get(pk = listing_id)
        #this will create/save the new comment
        new_comment = Comments(commentor = user, listings = listing,text = comment)
        new_comment.save()# we need to save it to the data base for later reference
        return HttpResponseRedirect(reverse("display_list",args=(listing_id,)))



def remove_watchlist(request, listing_id):
    user = request.user
    listing = AuctionList.objects.get(pk = listing_id)  
    listing.watchlist.remove(user) 

    messages.success(request,"-Watchlist removed Successfully!")
    """
    removing the link of the listing to the user.
    """
    #after removing the listing to the watchlist of the user it will stay at the display_list page
    return HttpResponseRedirect(reverse('display_list', args=(listing_id,)))

def closed_auction(request, listing_id):
    listing = AuctionList.objects.get(pk = listing_id)
    listing.is_closed = True
    listing.save()
    
    return HttpResponseRedirect(reverse('display_list', args=[listing_id]))

def place_bid(request,listing_id):
    if request.method == 'POST':
        listing = AuctionList.objects.get(pk= listing_id)
        new_bid = bid = int(request.POST['new_bid'])
        current_bid = listing.bid.bid

        if new_bid > current_bid:
            update_bid = Bid(bid= new_bid, user = request.user)
            update_bid.save()
            listing.bid = update_bid
            listing.save()
            messages.success(request,"Bid successfully added!")
            return HttpResponseRedirect(reverse('display_list',args=[listing_id]))
        else:
            messages.error(request,"Your Bid Denied! To LOW!")
            return HttpResponseRedirect(reverse('display_list',args=[listing_id]))


def watchlist(request): 
    user = request.user
    user_watchlist = user.watchlistings.all()
    return render(request, "auctions/watchlist.html",{
        'user_watchlist': user_watchlist
    })
    
    
def createlist(request):
    return render(request, "auctions/createlist.html")


def all_list(request):
    all_listings = AuctionList.objects.all()
    return render(request, "auctions/all_list.html",{
        'all_listings': all_listings
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



