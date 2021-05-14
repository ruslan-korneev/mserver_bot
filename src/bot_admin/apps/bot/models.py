from django.core.exceptions import ValidationError
from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        db_table = 'bot_project'

    def __str__(self):
        return self.title


STATUS_CHOICES = (
    ('admin', 'Admin'),
    ('collegue', 'Collegue'),
    ('user', 'User'),
)


class BotChatUser(models.Model):
    username = models.CharField(max_length=32, blank=True, null=True, editable=False)
    name = models.CharField(max_length=32, blank=True, null=True, editable=False)
    surname = models.CharField(max_length=32, blank=True, null=True, editable=False)
    chat_id = models.CharField(max_length=32, editable=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='user')
    subscribe = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return ("{} {}".format(self.name, self.surname))

    class Meta:
        db_table = 'bot_chat_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class BotServer(models.Model):
    host = models.CharField(max_length=15)
    username = models.CharField(max_length=32)
    path_to_key = models.FileField(upload_to='', verbose_name='Key-File',
                                   blank=True, null=True,
                                   help_text='Вставьте файл с ssh ключом')
    ssh_key = models.TextField(verbose_name='Key-Text', blank=True, null=True, help_text='Вставьте ssh ключ')
    project = models.ManyToManyField(Project, blank=True)
    alarm_status = models.BooleanField()

    def __str__(self):
        return ("{}@{}".format(self.username, self.host))

    def get_projects(self):
        return "\n".join([p.title for p in self.project.all()])

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        if not self.path_to_key and not self.ssh_key:
            raise ValidationError('Одно из полей должно быть заполнено! Key-File или Key-Text')

    class Meta:
        db_table = 'bot_server'
        verbose_name = 'Server'
        verbose_name_plural = 'Servers'


class BotUrl(models.Model):
    url = models.URLField()
    alarm_status = models.BooleanField()
    project = models.ManyToManyField(Project, blank=True)

    def __str__(self):
        return self.url

    def get_projects(self):
        return "\n".join([p.title for p in self.project.all()])

    class Meta:
        db_table = 'bot_url'
        verbose_name = 'Url'
        verbose_name_plural = 'Urls'
