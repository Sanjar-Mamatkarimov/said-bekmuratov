from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from .models import SiteSettings, Department, Event, Application, Reward, Teacher, Review, GalleryImage
from .forms import ApplicationForm, ReviewForm


def google_verification(request):
    """Файл подтверждения для Google Search Console (нужен в корне домена)."""
    return HttpResponse(
        'google-site-verification: googleb7b17b3ac980d512.html',
        content_type='text/html',
    )


def robots_txt(request):
    """robots.txt для поисковых систем."""
    sitemap_url = request.build_absolute_uri(reverse('django.contrib.sitemaps.views.sitemap'))
    content = f"User-agent: *\nAllow: /\nSitemap: {sitemap_url}\n"
    return HttpResponse(content, content_type='text/plain')

def get_context():
    """Базовый контент для всех страниц"""
    return {
        'settings': SiteSettings.objects.first(),
        'departments': Department.objects.all(),
        'events': Event.objects.all(),
        'rewards': Reward.objects.all().order_by('order'),
        'teachers': Teacher.objects.all().order_by('order'),
        'reviews': Review.objects.filter(is_published=True).order_by('-created_at'),
    }

def home(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        instrument = request.POST.get('instrument')
        application_type = request.POST.get('application_type', 'trial_lesson')

        Application.objects.create(
            name=name,
            phone=phone,
            instrument=instrument,
            application_type=application_type
        )
        messages.success(request, 'Ваша заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.')
        return redirect('home') 

    context = get_context()
    return render(request, 'home.html', context)

def teachers(request):
    context = get_context()
    return render(request, 'teachers.html', context)

def departments(request):
    context = get_context()
    return render(request, 'departments.html', context)

def events(request):
    context = get_context()
    return render(request, 'events.html', context)

def rewards(request):
    context = get_context()
    return render(request, 'rewards.html', context)

def contacts(request):
    # Получить тип заявки из GET параметра или по умолчанию
    application_type = request.GET.get('type', 'trial_lesson')
    
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        instrument = request.POST.get('instrument', '')
        age = request.POST.get('age', '')
        message = request.POST.get('message', '')
        application_type = request.POST.get('application_type', 'trial_lesson')

        if name and phone:
            Application.objects.create(
                name=name,
                phone=phone,
                instrument=instrument,
                age=int(age) if age else None,
                message=message,
                application_type=application_type
            )
            messages.success(request, 'Ваша заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.')
            return redirect('contacts')
        else:
            messages.error(request, 'Пожалуйста, заполните обязательные поля.')

    context = get_context()
    context['application_type'] = application_type
    return render(request, 'contacts.html', context)


def reviews(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Спасибо за ваш отзыв! Он будет опубликован после модерации.')
            return redirect('reviews')
    else:
        form = ReviewForm()
    
    context = get_context()
    context['form'] = form
    return render(request, 'reviews.html', context)


def gallery(request):
    context = get_context()
    context['gallery_images'] = GalleryImage.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'gallery.html', context)
