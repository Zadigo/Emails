import csv
import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from emailserver.patterns import construct_emails


class Home(TemplateView):
    template_name = 'hero/hero.html'

    def post(self, request, **kwargs):
        uploaded_file = request.FILES['file']
        storage = FileSystemStorage()
        storage.save(uploaded_file.name, uploaded_file)
        url = storage.url(uploaded_file.name)

        file_to_read = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
        with open(file_to_read, 'r', encoding='utf-8') as f:
            csv_content = csv.reader(f)
            data = list(csv_content).copy()
        def names():
            return data
        basic_patterns = construct_emails(names)
        return render(request, 'hero/hero.html', {'data': list(data), 'patterns': basic_patterns('.'), 'url': url})
