import time
import serial

# COMx for Windows
# /dev/ttyACMx for Linux
DEFAULT_COM = 'COM3'


class uC_interface():

	connected = False
	port = ''


	def __init__(self, COM=DEFAULT_COM, baudrate=115200):
		# Try to init connection
		try:
			self.com_port = serial.Serial(COM, baudrate)
			self.com_port.timeout = 5
			self.connected = True
		
		except Exception as e:
			pass


	# Reads one byte, blocking.
	# Expects to receive a GateState (str in range '0'..'5')
	# See gate.py and state machine diagram.
	def readMsg(self):
		try:
			msg = self.com_port.read()
			return msg
		except Exception as e:
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
		try:
			self.com_port.write(msg)
			return True
		except:
			return False


	def close(self):
		self.com_port.close()


	def sendSignal(Self):
		# Send signal message
		# In this case it is '0'
		return self.sendMsg('0')

	def requestState(self):
		# First send request state message
		# In this case it is '1'
		if self.sendMsg('1'):
			# Then receive
			state = readMsg()
			# Return as an int
			return int(state)

		# Error happened
		else:
			return -1

	


# --------------- Testing -------------------------

if __name__ == '__main__':
	uC = uC_interface()

	if uC.connected:
		print requestState()
