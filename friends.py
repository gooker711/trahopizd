import requests
import json
import random
from time import sleep
import traceback
from CONFIG import info

token=info.token#указать свой токен вк между ковычками
def main():
	try:
		zayavki=requests.get("https://api.vk.com/method/friends.getRequests?access_token=%s" % token+"&v=5.92").json()['response']['items']
		print(zayavki)
		requests.get("https://api.vk.com/method/friends.add?access_token=%s" % token+"&v=5.92&user_id="+str(random.choice(zayavki)))
	except:
		pass
	try:
		zayavki1=requests.get("https://api.vk.com/method/friends.getRequests?access_token=%s" % token+"&out=true&v=5.92").json()['response']['items']
		print(zayavki1)
		requests.get("https://api.vk.com/method/friends.delete?access_token=%s" % token+"&v=5.92&user_id="+str(random.choice(zayavki1)))
	except:
		pass
while True:
	try:
		main()
		sleep(10)
	except:
		pass