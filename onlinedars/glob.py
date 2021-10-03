from django.conf import settings
from django.urls import reverse
from django.utils.translation import activate

def lan(request):
    current_language = request.POST.get('lang')
    if current_language == settings.LANGUAGES[0][0]:
        reverse('users:home')
        activate('en')
    elif current_language == settings.LANGUAGES[1][0]:
        reverse('users:home')
        activate('uz')
    return {'languages':settings.LANGUAGES}