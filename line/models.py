from django.db import models
from .views import push_notify_text_message, get_token_status


class LineNotifyToken(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = 'Line通知Token'
    alias = models.CharField('別名', max_length=100)
    display_name = models.CharField('顯示名稱', max_length=100, blank=True)
    token = models.CharField('token', max_length=50)

    def __str__(self):
        return self.alias

    def save(self, *args, **kwargs):
        if not self.display_name:
            self.display_name = get_token_status(self.token).get('target')
        super().save(*args, **kwargs)

    def push_notify_text_message(self, message):
        push_notify_text_message(self.token, message)


class LineNotifyGroup(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = 'Line通知群組'
    name = models.CharField('名稱', max_length=100)
    members = models.ManyToManyField('LineNotifyToken', verbose_name='成員')

    def __str__(self):
        return self.name

    def push_group_message(self, message):
        for member in self.members.all():
            member.push_notify_text_message(message)
