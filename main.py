import time
import requests
from RPi import GPIO

# Constants

float_switch_pin = 1

class State():

	On = True
	Off = False

class Float_Switch():

	def __init__(self, pin):
		self.__pin = pin
		self.__state = self.get_state()
		
	def get_state(self):
		pass
		
class Notification():

	def __init__(self):
		pass
		
	def send(title, message):
		pass
		
def main():

	notification = Notification()
	float_switch = Float_Switch(float_switch_pin)
	
	while True:
		
		if float_switch.get_state() == State.On:
		
			
			notification.send("Water Dog", "Float Switch Has Been Triggered")
	
			while True:
			
				if float_switch.get_state() == State.Off:
					break
					
				time.sleep(1.0)
		time.sleep(1.0)
			

if __name__ == "__main__":
	main()
