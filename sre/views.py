import logging
import requests
from ipaddress import ip_address, ip_network
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from line.models import LineNotifyGroup
logger = logging.getLogger('debug')


@csrf_exempt
def status_cake_webhook(request):
    if request.method == 'POST':
        message = '\n{} - {}\n'.format(request.POST.get('Name'), request.POST.get('URL'))
        if request.POST.get('Status') == 'Up':
            message += 'Your site went back up!\n'
        elif request.POST.get('Status') == 'Down':
            message += 'Your site went down!\n'
        message += 'Code: ' + request.POST.get('StatusCode') + '\n'

        notify_group, created = LineNotifyGroup.objects.get_or_create(name='網站狀態通知')
        notify_group.push_group_message(message)

        client_ip = get_client_ip(request)
        whitelist = requests.get('https://app.statuscake.com/Workfloor/Locations.php?format=json').json()

        logger.debug(client_ip)
        for index, network in whitelist.items():
            if ip_address(client_ip) in ip_network(network.get('ip').replace(' ', '')):
                break
        else:
            logger.debug('{} not in whitelist.'.format(client_ip))
        return HttpResponse('success')
    raise Http404


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
