import json
import logging
import requests
from ipaddress import ip_address, ip_network
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt

from line.models import LineNotifyGroup
from .models import GitServer, RepositoryNotify
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


@csrf_exempt
def git_webhook(request):
    if request.method == 'POST':
        client_ip = get_client_ip(request)
        # Other git server
        git_server_ips = [lst[0] for lst in GitServer.objects.all().values_list('ip')]
        if client_ip in git_server_ips:
            payload = json.loads(request.body.decode('utf-8'))

            full_name = payload['repository']['name']
            for commit in payload['commits']:
                branch = payload['ref'].split('/')[-1]
                message = branch + '\n' + commit['message'] + '\n' + commit['author']['name']
                repository_notify = RepositoryNotify.objects.get(repository_fullname=full_name)
                repository_notify.push_notify(message)
            return HttpResponse('success')
        # Github
        whitelist = requests.get('https://api.github.com/meta').json()['hooks']
        for network in whitelist:
            if ip_address(client_ip) in ip_network(network):
                payload = json.loads(request.body.decode('utf-8'))

                full_name = payload['repository']['full_name']
                for commit in payload['commits']:
                    branch = payload['ref'].split('/')[-1]
                    if branch != 'master':
                        message = branch + '\n' + commit['message'] + '\n' + payload['pusher']['name']
                        repository_notify = RepositoryNotify.objects.get(repository_fullname=full_name)
                        repository_notify.push_notify(message)
                return HttpResponse('success')
        else:
            logger.debug('Not in white list:{}'.format(client_ip))
            return Http404


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
