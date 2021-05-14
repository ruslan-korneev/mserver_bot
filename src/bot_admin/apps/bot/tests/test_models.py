from django.test import TestCase
# from django.contrib.admin.sites import AdminSite
from apps.bot.models import Project, BotUrl, BotServer, BotChatUser
from apps.bot.admin import AdminUser, AdminServer, AdminUrl
from django.core.exceptions import ValidationError


class BotChatUserTest(TestCase):
	
	@classmethod
	def setUpTestData(cls):
		#Set up non-modified objects used by all test methods
		BotChatUser.objects.create(
			username='name-surname',
			name='Name',
			surname='Surname',
			chat_id='02385290',
			status='admin',
			subscribe=True)
	

	def test_chat_id_label(self):
		user = BotChatUser.objects.get(id=1)
		field_label = user._meta.get_field('chat_id').verbose_name
		self.assertEquals(field_label, 'chat id')


	def test_object_name(self):
	    user=BotChatUser.objects.get(id=1)
	    expected_object_name = "{} {} - {}".format(user.name, user.surname, user.status)
	    self.assertEquals(expected_object_name, str(user))


class BotServerTest(TestCase):

	@classmethod
	def setUpTestData(cls):
		#Set up non-modified objects used by all test methods
		BotServer.objects.create(
			host='0.0.0.0',
			username='bot',
			ssh_key='09g0uj4gj304gj3094g30g9jew',
			alarm_status=False)


	def test_object_name(self):
		server=BotServer.objects.get(id=1)
		expected_object_name = "{}@{}".format(server.username, server.host)
		self.assertEquals(expected_object_name, str(server))


	def test_validate_keys(self):
		server=BotServer.objects.get(id=1)
		self.assertRaisesMessage(ValidationError(message='Одно из полей должно быть заполнено! Key-File или Key-Text'), server.clean())


# class ProjectTest(TestCase):

# 	@classmethod
# 	def setUpTestData(cls):

# 		Project.objects.create(title='AMK')

# 		BotUrl.objects.create(
# 			url='vk.com',
# 			alarm_status=False,
# 			)

# 		BotServer.objects.create(
# 			host='127.0.0.1',
# 			username='bot',
# 			ssh_key='erpbmerperogj-2349tu952-f',
# 			alarm_status=False,
# 			project='AMK')


# 	def test_equals_project_title(self):
# 		project=Project.objects.get(id=1)
# 		url=BotUrl.objects.get(id=1)
# 		server=BotServer.objects.get(id=2)
# 		project_field_label = project._meta.get_field('title')
# 		server_field_label = server._meta.get_field('project')
# 		url_field_label = url._meta.get_field('project')
# 		self.assertEquals(server_field_label, url_field_label)
# 		self.assertEquals(server_field_label, project_field_label)
# 		self.assertEquals(url_field_label, project_field_label)
