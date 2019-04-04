#-*- coding: utf-8 -*-
from pyA20.gpio import gpio
from pyA20.gpio import port
import sys  
reload(sys)  
import time
import dht11
import datetime
from time import sleep
from flask import Flask, jsonify, render_template, request

from pyA20.gpio import gpio
from pyA20.gpio import port

gpio.init()

sys.setdefaultencoding('utf8')



app = Flask(__name__)

gpio.init()


pins = {
	8 : {'name' : 'Swiatlo', 'state' : gpio.HIGH},
	}





for pin in pins:
	gpio.setcfg(pin, gpio.OUTPUT)
	gpio.output(pin, gpio.HIGH)

@app.route("/")
def main():
	
	
	for pin in pins:
		pins[pin]['state'] = gpio.input(pin)
		
	templateData = {
		'pins' : pins
			
		}
	
	return render_template('index.html', **templateData)


@app.route("/_drzwi")
def drzwi():
	door_pin = 13
	gpio.setcfg(door_pin, gpio.INPUT)
	gpio.pullup(door_pin, gpio.PULLUP)

	if gpio.input(door_pin):
       	
		stan_gpio_drzwi = str('DRZWI SA ZAMKNIETE')
    	else:
       	stan_gpio_drzwi = str('DRZWI SA OTWARTE')
	
	return jsonify(stan_gpio_drzwi)


@app.route("/_okno")
def okno():
	window_pin = 14
	gpio.setcfg(window_pin, gpio.INPUT)
	gpio.pullup(window_pin, gpio.PULLUP)

	if gpio.input(window_pin):
		stan_gpio_okno = str('OKNO JEST OTWARTE')
    	else:
		stan_gpio_okno = str('OKNO JEST ZAMKNIETE')
	
	return jsonify(stan_gpio_okno)



@app.route("/_temp")
def temp():
	
	temp_pin = 12
	instance = dht11.DHT11(pin=temp_pin)
    	result = instance.read()
    	if result.is_valid():
			temperature = str(result.temperature)
	return jsonify(temperature)

@app.route("/_wilg")
def wilg():
	
	temp_pin = 12
	instance = dht11.DHT11(pin=temp_pin)
    	result = instance.read()
    	if result.is_valid():
		humidity = str(result.humidity)
	return jsonify(humidity)



@app.route("/<changePin>/<action>")
def action(changePin, action):
	name = 'OSWIETLENIE'
	changePin = int(changePin)
	deviceName = pins[changePin]['name']
	
	if action == "on":
		gpio.output(changePin, gpio.LOW)
		message = "Turned " + deviceName + " on."
	if action == "off":
		gpio.output(changePin, gpio.HIGH)
		message = "Turned " + deviceName + " off."
	
	for pin in pins:
		pins[pin]['state'] = gpio.input(pin)
	:
	templateData = {
		'pins' : pins,
			
		}

	return render_template('index.html', **templateData)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)
