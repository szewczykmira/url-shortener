# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from .forms import ShortURLForm
from .models import ShortURL


def home(request):
    """
    Homepage of app. Contains form for shortening links.
    """
    ctx = {'form': ShortURLForm(request.POST or None)}
    if request.method == 'POST':
        original_url = request.POST.get('original_url', False)
        contains_url = ShortURL.objects.filter(original_url=original_url)
        if contains_url.exists():
            messages.info(request, _("URL already was in our database!"))
            return redirect(reverse('display_info', kwargs={
                'short_url': contains_url.first().short_url
            }))
        if ctx['form'].is_valid():
            try:
                obj = ctx['form'].save()
                messages.success(request, _("Short link created!"))
                return redirect(reverse('display_info',
                                        kwargs={'short_url': obj.short_url}))
            except ObjectDoesNotExist:
                messages.error(request, _("An error occured"))

    return render(request, "url_shortener/home.html", ctx)


def follow_link(request, short_url):
    """
    Redirect to original url if it exists in database. If not then redirect to
    home page.
    """
    try:
        obj = ShortURL.objects.get(short_url=short_url)
        return redirect(obj.original_url)
    except ObjectDoesNotExist:
        messages.error(request, _("Link does not exists"))
        return redirect('home')


def display_info(request, short_url):
    """
    Displaying information about link. If it doesn't exists then
    returns to homepage
    """
    try:
        ctx = {
            'object': ShortURL.objects.select_related('user').get(
                short_url=short_url)
        }
    except ObjectDoesNotExist:
        messages.error(request, _("Link does not exists"))
        return redirect('home')
    return render(request, 'url_shortener/display_info.html', ctx)
