import threading
import requests
import os

from django.core.mail import EmailMessage
from django.http import JsonResponse, HttpResponse
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt

from SMTP_Project import settings


# Create your views here.


@csrf_exempt
def download_file(request):
    user_data = dict(
        cf_field_1=request.POST.get('cf_field_1'),
        cf_field_2=request.POST.get('cf_field_2'),
        ip=request.POST.get('ip'),
        tests=request.POST.get('cf_field_3')
    )
    data = dict(
        cw_attach=user_data['cf_field_1'],
        cf_field_2=user_data['cf_field_2'],
        cf_field_3=user_data['tests']
    )
    headers = dict(
        http_proxy_address=user_data['ip']
    )

    file_name = user_data['cf_field_1'] + '_' + user_data['cf_field_2'] + '_' + user_data['ip'] + '.pdf'
    path_to_file = os.path.join(settings.MEDIA_ROOT, file_name)
    r = requests.post('http://resmedlab.siroca.com:8084/Zakazresults.aspx', data=data, headers=headers)
    f = open(path_to_file, 'wb')
    f.write(r.content)
    f.close()

    with open(path_to_file, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/pdf")
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)

    os.remove(path_to_file)
    return response


@csrf_exempt
def send_to_mail(request):
    user_data = dict(
        cf_field_1=request.POST.get('cf_field_1'),
        cf_field_2=request.POST.get('cf_field_2'),
        ip=request.POST.get('ip'),
        tests=request.POST.get('cf_field_3')
    )
    print(user_data)
    data = dict(
        cw_attach=user_data['cf_field_1'],
        cf_field_2=user_data['cf_field_2'],
        cf_field_3=user_data['tests']
    )
    headers = dict(
        http_proxy_address=user_data['ip']
    )

    file_name = user_data['cf_field_1'] + '_' + user_data['cf_field_2'] + '_' + user_data['ip'] + '.pdf'
    path_to_file = os.path.join(settings.MEDIA_ROOT, file_name)
    r = requests.post('http://resmedlab.siroca.com:8084/Zakazresults.aspx', data=data, headers=headers)
    f = open(path_to_file, 'wb')
    f.write(r.content)
    f.close()

    kwargs = dict(
        to=[request.POST.get('email')],
        title='Получение результатов анализа',
        body=''
    )

    file = dict(
        path=path_to_file,
        name=file_name
    )
    send_file(kwargs, file)
    os.remove(file['path'])
    return JsonResponse(dict(status='SENT'))


def send_file(kwargs, file):
    title = kwargs.pop('title')
    mail = EmailMessage(title, **kwargs)
    mail.content_subtype = 'html'
    with open(file['path'], 'rb') as f:
        mail.attach(file['name'], f.read(), 'application/pdf')
        mail.send()
        f.close()
