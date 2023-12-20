import json
#import requests
import threading
import time
#from RPi import GPIO

# TODO: No longer needing test data

test_data = {}
lock = threading.Lock()

def update_test_data():
	global test_data
	while True:
		with open("test.json", "r") as file:
			try:
				new_test_data = json.load(file)
			except json.JSONDecodeError:
				continue
		
		with lock:
			test_data = new_test_data

		time.sleep(1)
		
thread = threading.Thread(target=update_test_data)
thread.daemon = True
thread.start()

time.sleep(5)
print("Using Test Data")

# Constants

relay_pin        = 1
float_switch_pin = 2
flow_sensor_pin  = 3

min_flow_rate = 1   #  1 l/min
max_flow_rate = 60  # 60 l/min

relay_timeout = 5.0 * 60.0  # 5 mins

secs_to_mins = 1/60

class State():

	On = True
	Off = False

class Relay():

	def __init__(self, pin):
		self.__pin = pin
		self.__state = State.Off
		
	def set_state(self, state):
		self.state = state
		
class Float_Switch():

	def __init__(self, pin):
		self.__pin = pin
		self.__state = self.get_state()
		
	def get_state(self):
		# TODO: Update with correct "GET"
		return test_data["FLOAT_SWITCH_STATE"] == "ON"
		
		
class Flow_Sensor():

	def __init__(self, pin):
		self.__pin = pin
		self.__rate = self.get_flow_rate()
		
	def get_flow_rate(self):
		# TODO: Update with correct "GET"
		return float(test_data["FLOW_SENSOR_FLOW_RATE"])

def main():

	relay = Relay(relay_pin)
	float_switch = Float_Switch(float_switch_pin)
	flow_sensor = Flow_Sensor(flow_sensor_pin)
	
	while True:
		
		if float_switch.get_state() == State.On:
		
			print("Notify Pump Was Turned On")
			relay.set_state(State.On)
			
			litters_pumped = 0.0
			relay_start_time = time.time()
			relay_previous_time = relay_start_time
			
			while True:
			
				relay_current_time = time.time()
				
				time_delta = relay_current_time - relay_previous_time
								
				flow_rate = flow_sensor.get_flow_rate()
				
				litters_pumped += flow_rate * time_delta * secs_to_mins
							
				if relay_current_time > relay_start_time + relay_timeout:
					print("Notify Pump Was Turned Off By Timeout")
					break
			
				if float_switch.get_state() == State.Off and flow_rate <= min_flow_rate:
					print("Notify Pump Was Turned Off By Float Switch And Flow Sensor")
					break
					
				relay_previous_time = relay_current_time
			
			print("Notify %f Litters Of Water Was Pumped" % litters_pumped)
			relay.set_state(State.Off)

if __name__ == "__main__":
	main()
