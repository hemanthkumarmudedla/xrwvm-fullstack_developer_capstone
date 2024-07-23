# Uncomment the imports before you add the code
from django.urls import path # type: ignore
from django.conf.urls.static import static # type: ignore
from django.conf import settings # type: ignore
from django.views.generic import TemplateView # type: ignore
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # # path for registration
    path(route='register', view=views.registration, name='register'),
    # path for login
    path(route='login', view=views.login_user, name='login'),

    # path for logout
    path(route='logout', view=views.logout_request, name='logout'),

    path(route='get_cars', view=views.get_cars, name ='get_cars'),

    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
