# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime
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
    # Try to check if provide credential can be authenticated
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

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
# ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request):
# ...
