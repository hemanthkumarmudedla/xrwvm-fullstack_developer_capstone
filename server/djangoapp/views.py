# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime

from djangoapp.restapis import analyze_review_sentiments, get_request, post_review
from .models import CarMake, CarModel
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provided credentials can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Create a `logout_request` view to handle sign out request
@csrf_exempt
def logout_request(request):
    logout(request)
    data = {"userName":""}
    return JsonResponse(data)

# Create a `registration` view to handle sign up request
from django.core.exceptions import ObjectDoesNotExist

@csrf_exempt
def registration(request):
    context = {}

    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get('userName')
        password = data.get('password')
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        email = data.get('email')

        if not all([username, password, first_name, last_name, email]):
            return JsonResponse({"error": "All fields are required"}, status=400)

        try:
            # Check if user already exists
            User.objects.get(username=username)
            return JsonResponse({"error": "Username already exists"}, status=400)
        except ObjectDoesNotExist:
            try:
                # Check if email already exists
                User.objects.get(email=email)
                return JsonResponse({"error": "Email already registered"}, status=400)
            except ObjectDoesNotExist:
                # Create user in auth_user table
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password, email=email)
                # Login the user
                login(request, user)
                return JsonResponse({"userName": username, "status": "Authenticated"})

    return JsonResponse({"error": "Invalid request method"}, status=405)

def get_cars(request):
    count = CarMake.objects.count()
    initiate()
    car_models = CarModel.objects.select_related('make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.make.name})
    return JsonResponse({"CarModels": cars})

# Update the `get_dealerships` render list of dealerships all by default, particular state if state is passed
def get_dealerships(request, state="All"):
    if(state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/"+state
    dealerships = get_request(endpoint)
    return JsonResponse({"status":200,"dealers":dealerships})

def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchDealer/"+str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status":200,"dealer":dealership})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})

def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        print(f"Requesting reviews from endpoint: {endpoint}")  # Debugging print
        try:
            # Fetch reviews from the endpoint
            reviews = get_request(endpoint)
            print(f"Received reviews: {reviews}")  # Debugging print
            
            # Check if reviews are successfully fetched
            if reviews:
                # Analyze sentiments
                sentiments = analyze_review_sentiments(reviews)
                print(f"Sentiments analysis result: {sentiments}")  # Debugging print
                return JsonResponse({"status": 200, "reviews": sentiments})
            else:
                print("No reviews found")  # Debugging print
                return JsonResponse({"status": 404, "message": "No reviews found"})
        except Exception as e:
            logger.error(f"Error fetching or analyzing reviews: {e}")
            print(f"Unexpected error occurred: {e}")  # Debugging print
            return JsonResponse({"status": 500, "message": "Internal Server Error"})
    else:
        print("Invalid dealer_id")  # Debugging print
        return JsonResponse({"status": 400, "message": "Bad Request"})

def add_review(request):
    if(request.user.is_anonymous == False):
        data = json.loads(request.body)
        try:
            # Post the review and get the response
            post_response = post_review(data)
            
            # Extract the review ID from the response if available
            review_id = post_response.get('id')
            
            # Analyze sentiment of the review
            sentiments = analyze_review_sentiments([data])
            
            # Combine the review response with sentiment analysis
            result = {
                "status": 200,
                "review": post_response,
                "sentiments": sentiments[0] if sentiments else None
            }
            return JsonResponse(result)
        except:
            return JsonResponse({"status":401,"message":"Error in posting review"})
    else:
        return JsonResponse({"status":403,"message":"Unauthorized"})
