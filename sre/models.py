from django.db import models
from line.models import LineNotifyToken, LineNotifyGroup


class GitServer(models.Model):
    name = models.CharField('名稱', max_length=50)
    ip = models.CharField('ip', max_length=20)

    def __str__(self):
        return self.name


class RepositoryNotify(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = 'Line通知token'
    repository_fullname = models.CharField('Repository全名', max_length=100)
    secret = models.CharField('Webhook secret', max_length=50, blank=True)
    notify = models.ForeignKey(LineNotifyToken, verbose_name='通知', on_delete=False, blank=True, null=True)
    notify_group = models.ForeignKey(LineNotifyGroup, verbose_name='通知群組', on_delete=False, blank=True, null=True)

    def __str__(self):
        return self.repository_fullname
    
    def push_notify(self, message):
        if self.notify:
            self.notify.push_notify_text_message(message)
        if self.notify_group:
            self.notify_group.push_group_message(message)
