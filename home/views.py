from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.utils.translation import activate, get_language, gettext
from django.utils import translation
from .models import Partner, ContactUs, Order, Blog, TruckType

# Create your views here.

def lang(request):
    if 'POST' == request.method:
        language = request.POST.get('language')
        activate(language)
        request.session[settings.LANGUAGE_CODE] = language
        # print(language)
        return redirect('home')


def home(request):
    partners = Partner.objects.all()
    blogs = Blog.objects.all()
    truck_types = TruckType.objects.all()
    context = {'partners': partners, 'blogs': blogs, 'truck_types': truck_types}
    return render(request, 'index.html', context)


def contact(request):
    if 'POST' == request.method:
        name = request.POST.get('first_name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        ContactUs.objects.create(name=name, email=email, subject=subject, message=message)

        return redirect('home')

    return redirect('home')


def order(request):
    if 'POST' == request.method:
        from_where = request.POST.get('from_where')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        to_where = request.POST.get('to_where')
        weight = request.POST.get('weight')

        when = request.POST.get('when')
        truck_type = request.POST.get('truck_type')
        truck_type = get_object_or_404(TruckType, id=truck_type)

        Order.objects.create(from_where=from_where,phone=phone , email=email ,to_where=to_where, weight=weight, when=when, truck_type=truck_type)

        return redirect('home')

    return redirect('home')
