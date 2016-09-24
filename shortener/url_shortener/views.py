# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from .forms import ShortURLForm
from .models import ShortURL


def home(request):
    ctx = {'form': ShortURLForm(request.POST or None)}
    if request.method == 'POST':
        origin_url = request.POST.get('origin_url', False)
        contains_url = ShortURL.objects.filter(original_url=origin_url)
        if contains_url.exists():
            messages.info(request, _("URL already was in our database!"))
            # TODO redirect
        if ctx['form'].is_valid():
            try:
                obj = ctx['form'].save()
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
        messages.error(request, _("There is not the link you are looking for"))
        return redirect('home')
