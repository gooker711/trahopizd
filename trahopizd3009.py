# -*- coding: utf-8 -*-
import requests, vk_api, random,time,traceback
from threading import Thread
from info import info
from pod import pod
from vk_api.longpoll import VkLongPoll, VkEventType, VkChatEventType
from python3_anticaptcha import ImageToTextTask
from python3_anticaptcha import errors

class MyThread2(Thread):
	def __init__(self, name,captcha_key):
		Thread.__init__(self)
		self.name = name
		self.captcha_key = captcha_key
	def run(self):
		def captcha_handler(captcha):
			key = ImageToTextTask.ImageToTextTask(anticaptcha_key=self.captcha_key, save_format='const') \
					.captcha_handler(captcha_link=captcha.get_url())
			return captcha.try_again(key['solution']['text'])
		token=self.name
		vk_session = vk_api.VkApi(token=token, captcha_handler=captcha_handler)
		vk = vk_session.get_api()
		a=requests.get("https://api.vk.com/method/users.get?access_token="+self.name+"&v=5.92").json()
		name=a['response'][0]['first_name']
		surname=a['response'][0]['last_name']
		print(name+" "+surname+" добавляет в друзья")
		for idd in info.ids:
			try:
				vk.friends.add(user_id=idd)
			except:
				pass
		else:
			print(name+" "+surname+" добавил в друзья!")

class MyThread(Thread):
	def __init__(self, name):
		Thread.__init__(self)
		self.name = name
	def run(self):
		vk_session = vk_api.VkApi(token=self.name)
		vk = vk_session.get_api()
		longpoll = VkLongPoll(vk_session)
		while True:
			try:
				for event in longpoll.listen():
					if event.type_id == VkChatEventType.USER_KICKED:
						requests.get("https://api.vk.com/method/messages.addChatUser?access_token="+self.name+"&v=5.92&chat_id="+str(event.chat_id)+"&user_id="+str(event.info['user_id']))
			except:
				pass

class MyThread4(Thread):
	def __init__(self, name):
		Thread.__init__(self)
		self.name = name
	def run(self):
		vk_session = vk_api.VkApi(token=self.name)
		vk = vk_session.get_api()
		longpoll = VkLongPoll(vk_session)
		while True:
			try:
				for event in longpoll.listen():
					if event.type == VkEventType.MESSAGE_NEW and not event.user_id in info.ids and event.text == "start":
						while True:
							try:
								time.sleep(random.randint(2,5))
								titled=vk.messages.getChat(chat_id=event.chat_id)['title']
								if titled == info.title:
									try:
										vk.messages.unpin(peer_id=event.peer_id)
									except:
										pass
									try:
										vk.messages.deleteChatPhoto(chat_id=event.chat_id)
									except:
										pass
									a=vk.messages.send(random_id=random.randint(100000,999999),chat_id=event.chat_id,message="Привет")
									vk.messages.edit(peer_id=event.peer_id,message=info.msg,message_id=a)
								if titled != info.title:
									a=vk.messages.send(random_id=random.randint(100000,999999),chat_id=event.chat_id,message="Привет")
									vk.messages.edit(peer_id=event.peer_id,message=info.msg,message_id=a)
									vk.messages.editChat(chat_id=event.chat_id,title=info.title)
									try:
										vk.messages.deleteChatPhoto(chat_id=event.chat_id)
									except:
										pass
									try:
										vk.messages.unpin(peer_id=event.peer_id)
									except:
										pass
							except:
								pass
			except:
				pass

class MyThread3(Thread):
	def __init__(self, name):
		Thread.__init__(self)
		self.name = name
	def run(self):
		vk_session = vk_api.VkApi(token=self.name)
		vk = vk_session.get_api()
		longpoll = VkLongPoll(vk_session)
		while True:
			try:
				for event in longpoll.listen():
					if event.type == VkEventType.MESSAGE_NEW and not event.user_id in info.ids and event.text == "start":
						while True:
							try:
								time.sleep(random.randint(2,5))
								a=vk.messages.send(random_id=random.randint(100000,999999),chat_id=event.chat_id,message="Привет")
								vk.messages.edit(peer_id=event.peer_id,message=info.msg,message_id=a)
							except:
								pass
			except:
				pass

while True:
	try:
		a=int(input('\nВыберите функцию:\n\n1.Запустить антикик и спам, если все последующие пункты проделаны\n2.Сгенерировать конфиг с токенами, загрузить текст из файла  "message.txt" и записать название беседы, которое поставят боты\n3.Зайти в конфу по ссылке\n4.Пригласить в конфу с главного акка\n5.Добавить друг друга в др\n6.Добавить пользователя в антикик\n7.Убрать пользователя из антикика\n8.Флуд в лс\n9.Сбросить каптчи на акках, если боты перестали флудить\n10.Получить токен для инвайта рейд ботов\n11.Пригласить рейд ботов\n12.Пригласить рейд ботов через баг\n13.Наш рейд бот для спама в конфах\n14.Исключить всех участников беседы\n15.Очистить группу вк от подпищиков\n16.Почистить стену вк\n17.Заспамить стену\n18.Заспамить комментарии\n19.Удаление всех комментариев\n20.Автосмена паролей аккаунтов в acc.txt\n\n'))
		if a == 1:
			print('Выйти из антикика вы сможете только закрыв окно с терминалом или нажав ctrl+c\nАктивировать спам можно командой start с акка любого бота\nЗапускается антикик...')
			choice=int(input('Выберите:\n1.Просто антикик\n2.Антикик+спам\n3.Антикик + спам + смена названия конфы\n4.Спам + смена названия\n5.Только спам!\n\n'))
			if choice == 1:
				for i in range(len(info.tokenlist)):
						name = info.tokenlist[i]
						my_thread = MyThread(name)
						my_thread.start()
				else:
					print('Антикик запущен!')
			if choice == 2:
				for i in range(len(info.tokenlist)):
						name = info.tokenlist[i]
						my_thread = MyThread3(name)
						my_thread.start()
						my_thread = MyThread(name)
						my_thread.start()
				else:
					print('Антикик + спам запущен!')
			if choice == 3:
				for i in range(len(info.tokenlist)):
						name = info.tokenlist[i]
						my_thread = MyThread4(name)
						my_thread.start()
						my_thread = MyThread(name)
						my_thread.start()
				else:
					print('Антикик + спам + смена названия запущены!')
			if choice == 4:
				for i in range(len(info.tokenlist)):
						name = info.tokenlist[i]
						my_thread = MyThread4(name)
						my_thread.start()
				else:
					print('Спам + смена названия запущены!')
			if choice == 5:
				for i in range(len(info.tokenlist)):
						name = info.tokenlist[i]
						my_thread = MyThread3(name)
						my_thread.start()
				else:
					print('Спам запущен!')
		if a == 2:
			try:
				print('Генерация конфига...')
				accs=len(open('acc.txt', 'r',encoding='utf8').readlines())
				k=open('info.py',"wt")
				k.write('class info():\n	tokenlist =[')
				k.close()
				print('генерация токенов')
				for x in range (accs):
					f=open('acc.txt',encoding='utf8').read()
					num_and_passwd=f.split('\n')[x]
					b=num_and_passwd.find(':')
					phone=num_and_passwd[0:b]
					passwd=num_and_passwd[b+1:len(num_and_passwd)]
					try:
						f=requests.get("https://oauth.vk.com/token?grant_type=password&client_id=2274003&client_secret=hHbZxrka2uZ6jB1inYsH&username=" + str(phone) + "&password=" + str(passwd))
						print(f)
						k=open('info.py',"at",encoding='utf8')
						k.write('"'+str(f.json()["access_token"])+'",')
						k.close()
					except:
						a=open('info.py',"wt")
						a.write('class info():\n	token=[]')
						a.close()
						pass
				else:
					k=open('info.py',"rt",encoding='utf8').read()
					text=k[0:len(k)-1]
					a=open('info.py',"wt",encoding='utf8')
					a.write(text+"]")
					a.close()
				k=open('info.py',"at",encoding='utf8')
				k.write('\n	ids =[')
				k.close()
				print('генерация айди')
				for x in range (accs):
					f=open('acc.txt',encoding='utf8').read()
					num_and_passwd=f.split('\n')[x]
					b=num_and_passwd.find(':')
					phone=num_and_passwd[0:b]
					passwd=num_and_passwd[b+1:len(num_and_passwd)]
					try:
						f=requests.get("https://oauth.vk.com/token?grant_type=password&client_id=2274003&client_secret=hHbZxrka2uZ6jB1inYsH&username=" + str(phone) + "&password=" + str(passwd))
						k=open('info.py',"at",encoding='utf8')
						k.write('"'+str(f.json()["user_id"])+'",')
						k.close()
					except:
						print("Акк в файле 'acc.txt', строка "+str(x+1)+" выдаёт ошибку. Может неправильный логин и пароль, а мб заблокировали\nЖелательно убрать эти акки и перезапустить генерацию")
						a=open('info.py',"wt",encoding='utf8')
						a.write('class info():\n	token=[]')
						a.close()
						exit()
				else:
					print("установка сообщения")
					k=open('info.py',"rt",encoding='utf8').read()
					text=k[0:len(k)-1]
					text1=open('message.txt',"rt",encoding='utf8').read()
					a=open('info.py',"wt",encoding='utf8')
					a.write(text+"]\n	msg='"+text1+"'\n	title='"+input('Сообщение для спама у вас теперь обновлено в файле "message.txt". Введите название беседы, какое будет при рейде: ')+"'")
					a.close()
					print('Готово! Перезапустите скрипт!')
			except:
				a=open('info.py',"wt",encoding='utf8')
				a.write('class info():\n	token=[]')
				a.close()
				print('\nВы неправильно ввели данные')
		if a == 3:
			link=input('Ссылка на беседу: ')
			print('Заход в конфу...')
			for user in info.tokenlist:
				requests.get("https://api.vk.com/method/messages.joinChatByInviteLink?access_token="+user+"&v=5.92&link="+link)
			else:
				print('Все зашли!')
		if a == 4:
			print('Главный акк - ваш аккаунт, с которого вам надо пригласить всех в конфу\nУказывайте его логин и пароль в первой строке')
			owner=info.tokenlist[0]
			chat=input('введите айди беседы: ')
			print('Запуск')
			for acc in info.ids:
				requests.get("https://api.vk.com/method/messages.addChatUser?access_token="+owner+"&v=5.92&chat_id="+chat+"&user_id="+acc)
			else:
				print('Все приглашены!')
		if a == 5:
			captcha_key=input('Ключ от "https://anti-captcha.com/": ')
			for x in range(len(info.tokenlist)):
				name = info.tokenlist[x]
				my_thread = MyThread2(name,captcha_key)
				my_thread.start()
		if a == 6:
			captcha_key=input('Ключ от "https://anti-captcha.com/": ')
			iduser=input('Айди пользователя, которого вы хотите добавить в антикик: ')
			def captcha_handler(captcha):
				key = ImageToTextTask.ImageToTextTask(anticaptcha_key=captcha_key, save_format='const') \
						.captcha_handler(captcha_link=captcha.get_url())
				return captcha.try_again(key['solution']['text'])
			for token in info.tokenlist:
				try:
					vk_session = vk_api.VkApi(token=token, captcha_handler=captcha_handler)
					vk = vk_session.get_api()
					vk.friends.add(user_id=iduser)
				except:
					pass
			else:
				print('Пользователю отправлены заявки друзья. Когда он их примит, он будет добавлен в антикик')
		if a == 7:
			iduser=input('Айди пользователя, которого вы хотите убрать из антикика: ')
			for token in info.tokenlist:
				requests.get("https://api.vk.com/method/friends.delete?access_token="+token+"&v=5.92&user_id="+iduser)
			else:
				print('Пользователь убран из антикика')
		if a == 8:
			iduser=input('Айди того, кому надо засрать лс: ')
			while True:
				for token in info.tokenlist:
					try:
						vk_session = vk_api.VkApi(token=token)
						vk = vk_session.get_api()
						vk.messages.send(user_id=iduser,message=info.msg,random_id=random.randint(100000,999999))
					except:
						pass
				else:
					print('Все акки отправили по ссобщению. Шлют собщения бесконечно')
		if a == 9:
			captcha_key=input('Ключ от "https://anti-captcha.com/": ')
			def captcha_handler(captcha):
				key = ImageToTextTask.ImageToTextTask(anticaptcha_key=captcha_key, save_format='const') \
						.captcha_handler(captcha_link=captcha.get_url())
				return captcha.try_again(key['solution']['text'])
			for x in range (len(info.tokenlist)):
				try:
					token=info.tokenlist[x]
					iduser=info.ids[x]
					vk_session = vk_api.VkApi(token=token, captcha_handler=captcha_handler)
					vk = vk_session.get_api()
					vk.messages.send(user_id=iduser,message=".",random_id=random.randint(100000,999999))
					vk.messages.editChat(chat_id=1,title=".",random_id=random.randint(100000,999999))
				except:
					pass
			else:
				print('Акки очищены от каптч!')
		if a == 10:
			try:
				print('Чтобы получить токен для инвайта рейд ботов да и других ботов, вам нужно перейти по ссылке\nhttps://oauth.vk.com/authorize?client_id=6441755&scope=notify%2Cphotos%2Cfriends%2Caudio%2Cvideo%2Cnotes%2Cpages%2Cdocs%2Cstatus%2Cquestions%2Coffers%2Cwall%2Cgroups%2Cnotifications%2Cstats%2Cads%2Coffline&redirect_uri=https://api.vk.com/blank.html&display=page&response_type=token&revoke=1\nИ подтвердить. А потом вставить новый токен, который сгенерировался в браузере')
				token=input("Вставьте токен из новой ссылки, он начинается от 'access_token=' и заканчивается до '&expires_in': ")
				print('Запись токена в конфиг')
				a=open('pod.py',"wt",encoding='utf8')
				a.write("class pod():\n	token='"+token+"'"+"\n	idbots=["+input("запишите айди групп через запятую с минусом:\n")+"]")
				a.close()
				print("Токен добавлен и id записаны! Перезапустите скрипт")
			except:
				a=open('pod.py',"wt",encoding='utf8')
				a.write("class pod():\n	token=''")
				a.close()
				print("Вы неправильно вставили данные")
		if a == 11:
			idconf=str(2000000000+int(input('Введите айди беседы для приглашения ботов: ')))
			print("Приглашение ботов в беседу")
			try:
				token=pod.token
				for x in pod.idbots:
					requests.get("https://api.vk.com/method/bot.addBotToChat?access_token="+token+"&peer_id="+idconf+"&bot_id="+str(x)+"&v=5.92")
				else:
					print("Боты приглашены!")
			except:
				print("Заполните конфигурацию для приглашения в пункте 10")
		if a == 12:
			idconf=str(2000000000+int(input('Введите айди беседы для приглашения ботов: ')))
			print("Приглашение ботов в беседу")
			try:
				token=pod.token
				for x in pod.idbots:
					requests.get("https://api.vk.com/method/bot.addBotToChat?access_token="+token+"&peer_id="+idconf+"&bot_id="+str(x)+"&v=5.92")
					time.sleep(1)
					requests.get("https://api.vk.com/method/bot.kickBot?access_token="+token+"&peer_id="+idconf+"&bot_id="+str(x)+"&v=5.92")
				else:
					print("Боты приглашены!")
			except:
				print("Заполните конфигурацию для приглашения в пункте 11")
		if a == 13:
			print('У нас есть свой рейд бот. Он платный, но плата даёт вам возможность получить быстрый спам от 900 сообщений и до больше тысячи\nhttps://t.me/bot_drochila - ссылка на него')
		if a == 14:
			print('Главный акк - ваш аккаунт, с которого вам надо кикнуть всех участников в беседе\nУказывайте его логин и пароль в первой строке')
			owner=info.tokenlist[0]
			chat=input('введите айди беседы: ')
			a=requests.get("https://api.vk.com/method/messages.getChat?access_token="+owner+"&chat_id="+chat+"&v=5.92").json()['response']['users']
			print('Запуск')
			while True:
				try:
					for i in a:
						if i != int(info.ids[0]):
							requests.get("https://api.vk.com/method/messages.removeChatUser?access_token="+owner+"&chat_id="+chat+"&member_id="+str(i)+"&v=5.92").json()
				except:
					pass
		if a == 15:
			token=info.tokenlist[0]
			group_id=input('Айди группы без минуса: ')

			class MyThread(Thread):
				def __init__(self, i):
					Thread.__init__(self)
					self.i = i
				def run(self):
					print("Удалён "+str(self.i))
					a=requests.get("https://api.vk.com/method/groups.removeUser?access_token="+token+"&group_id="+group_id+"&user_id="+str(self.i)+"&v=5.92").json()
					print(a)
			a=requests.get("https://api.vk.com/method/groups.getMembers?access_token="+token+"&group_id="+group_id+"&v=5.92").json()['response']['items']
			while True:
				for i in a:
					try:
						my_thread = MyThread(i)
						my_thread.start()
						time.sleep(0.05)
					except:
						pass
		if a == 16:
			class MyThread(Thread):
				def __init__(self, x,owner,token):
					Thread.__init__(self)
					self.x = x
					self.owner = owner
					self.token = token
				def run(self):
					requests.get("https://api.vk.com/method/wall.delete?access_token=%s" % str(token)+"&owner_id="+str(owner)+"&post_id="+str(x)+"&v=5.92")
			token=info.tokenlist[0]
			owner=input("Айди страницы (без минуса) или айди группы с минусом, чтобы всё удалить: \n")
			a=requests.get("https://api.vk.com/method/wall.get?access_token=%s" % str(token)+"&owner_id="+str(owner)+"&count=1&v=5.92").json()['response']['items'][0]['id']
			for x in sorted(list(range(a+1)), reverse = True):
				print("Удалён пост - wall"+str(owner)+str("_")+str(x))
				my_thread = MyThread(x,token,owner)
				my_thread.start()
				time.sleep(0.5)
			else:
				print("Всё удалено!")
				pass
		if a == 17:
			class MyThread(Thread):
				def __init__(self,x,wall):
					Thread.__init__(self)
					self.x = x
					self.wall = wall
				def run(self):
					vk_session = vk_api.VkApi(token=self.x)
					vk = vk_session.get_api()
					vk.wall.post(owner_id=wall,message=info.msg)
			wall=input("Айди страницы (без минуса) или айди группы с минусом, чтобы заспамить: \n")
			print('Спам начался!')
			for x in info.tokenlist:
				for a in range(10):
					my_thread = MyThread(x,wall)
					my_thread.start()
					time.sleep(1)
			else:
				print('Спам завершился!')
		if a == 18:
			class MyThread(Thread):
				def __init__(self,x,wall,idpost):
					Thread.__init__(self)
					self.x = x
					self.wall = wall
					self.idpost = idpost
				def run(self):
					vk_session = vk_api.VkApi(token=self.x)
					vk = vk_session.get_api()
					vk.wall.createComment(owner_id=wall,post_id=idpost,message=info.msg)
			wall=input("Айди страницы (без минуса) или айди группы с минусом, чтобы заспамить: \n")
			idpost=input("Айди поста (находится в ссылке на пост после _ \n")
			print('Спам начался в комментарии!')
			for x in info.tokenlist:
				for a in range(10):
					my_thread = MyThread(x,wall,idpost)
					my_thread.start()
					time.sleep(1)
			else:
				print('Спам завершился!')
		if a == 19:
			class MyThread(Thread):
				def __init__(self, x,owner,token):
					Thread.__init__(self)
					self.x = x
					self.owner = owner
					self.token = token
				def run(self):
					requests.get("https://api.vk.com/method/wall.deleteComment?access_token=%s" % str(token)+"&owner_id="+str(owner)+"&comment_id="+str(x)+"&v=5.92")
			token=info.tokenlist[0]
			owner=input("Айди страницы (без минуса) или айди группы с минусом, чтобы удалить комментарии: \n")
			idpost=input("Айди поста (находится в ссылке на пост после _ \n")
			a=requests.get("https://api.vk.com/method/wall.getComments?access_token=%s" % str(token)+"&owner_id="+str(owner)+"&post_id="+idpost+"&count=1&v=5.92").json()['response']['items'][0]['id']
			count=requests.get("https://api.vk.com/method/wall.getComments?access_token=%s" % str(token)+"&owner_id="+str(owner)+"&post_id="+idpost+"&count=1&v=5.92").json()['response']['count']
			for x in range(int(a),int(a)+int(count)):
				print("Удалён комментарий - wall"+str(owner)+str("_")+str(x))
				my_thread = MyThread(x,token,owner)
				my_thread.start()
				time.sleep(0.5)
			else:
				print("Комментарии удалены!")
				pass

		if a == 20:
			newparol=input("Перед тем, как менять пароли на купленных акках, выполните пункт 2 в меню\nНовый пароль для аккаунтов:\n")
			print("Смена паролей началась:\n")
			for x in range(len(info.tokenlist)):
				try:
					token=info.tokenlist[x]
					print("Смена пароля на "+str(x+1)+" акке")
					f=open('acc.txt').read()
					num_and_passwd=f.split('\n')[x]
					b=num_and_passwd.find(':')
					passwd=num_and_passwd[b+1:len(num_and_passwd)]
					a=requests.get("https://api.vk.com/method/account.changePassword?access_token=%s" % str(token)+"&old_password="+str(passwd)+"&new_password="+newparol+"&v=5.92").json()['response']
					print(a)
					time.sleep(1)
				except:
					print(str(x+1)+" пароль не сменен")
					pass
			else:
				print("Смена паролей звершена! Осталось только в acc.txt все старые пароли заменить на 1 новый, который вы написали!")
	except:
		exit()
