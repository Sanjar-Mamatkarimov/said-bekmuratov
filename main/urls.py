from django.urls import path
from .views import home, teachers, departments, events, rewards, contacts, reviews, gallery, google_verification, robots_txt

urlpatterns = [
    path('', home, name='home'),
    path('teachers/', teachers, name='teachers'),
    path('departments/', departments, name='departments'),
    path('events/', events, name='events'),
    path('rewards/', rewards, name='rewards'),
    path('contacts/', contacts, name='contacts'),
    path('reviews/', reviews, name='reviews'),
    path('gallery/', gallery, name='gallery'),
    path('googleb7b17b3ac980d512.html', google_verification, name='google_verification'),
    path('robots.txt', robots_txt, name='robots_txt'),
]