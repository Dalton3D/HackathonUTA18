import requests
from time import sleep

ip = "192.168.0.100"  #TESTING

# get user key
url = "http://"+ip+"/api"
info = {"devicetype": "hack_proj#mpzinke"}
usr_data = requests.post(url, json=info)
usr = usr_data.text[usr_data.text.find(":{\"username\":\"")+14:len(usr_data.text)-4]

usr = "-rAVGu8Iwm5BXEydsHoCLSDfg8zDU9eLjit9DKaq"

url += usr

lights = requests.get(url + "/lights")

# for being awesome
number_of_lights = 3
for i in range(number_of_lights, 4):
	requests.put(url + "/lights/" + str(i) + "/state", json={"hue" : 1, "sat": 254})	
	sleep(3)
	requests.put(url + "/lights/" + str(i) + "/state", json={"on" : False})