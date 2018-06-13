import time
import serial

# COMx for Windows
# /dev/ttyACMx for Linux
DEFAULT_COM = 'COM3'


class uC_interface():

	connected = False

	def __init__(self, COM=DEFAULT_COM, baudrate=115200):
		# Try to init connection
		try:
			self.com_port = serial.Serial(COM, baudrate)
			self.com_port.timeout = 5
			self.connected = True
		
		except Exception as e:
			print(e)
			pass


	# Reads one byte, blocking.
	# Expects to receive a GateState (str in range '0'..'5')
	# See gate.py and state machine diagram.
	def readMsg(self):
		try:
			msg = self.com_port.read()
			return chr( msg )	# Converts btye to str (eg. 48 to '0'. Try: ord('0'))
		except Exception as e:
			print(e)
			return -1

		return msg
		# Note: if using other protocol, transform the received
		# message to the GateState model for it to be compatible
		# with the GUI.


	# Sends one byte, blocking.
	# Sends as a string
	# (e.g.: if msg=0, then '0' is sent)
	def sendMsg(self, msg):
		msg = str(msg)
		msg = bytes(msg, 'utf8')
		try:
			self.com_port.write(msg)
			return True
		except Exception as e:
			print(e)
			return False


	def close(self):
		try:
			self.com_port.close()
		except Exception as e:
			print(e)
			pass


	# Send "remote control" signal.
	def sendSignal(self):
		# Send signal message
		# In this case it is '0'
		return self.sendMsg('0')


	def requestState(self):
		# First send request state message
		# In this case it is '1'
		if self.sendMsg('1'):	# If successful
			# Then receive
			state = self.readMsg()
			# Return as an int to be consistent with GateStates
			return int(state)

		# Error happened
		else:
			return -1

	


# --------------- Testing -------------------------

if __name__ == '__main__':
	uC = uC_interface()
	assert uC.connected, 'Connection failed'

	print(requestState())

	uC.sendSignal()

	for i in range(5):
		print(uc.requestState())
		time.sleep(1)
