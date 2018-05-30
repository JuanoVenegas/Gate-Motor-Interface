
import time
from threading import Timer
import gate as g

GS = g.GateStates
TRANSITION_DURATION = 2.5

class uC_interface():

	connected = False
	gate = g.Gate(GS.Closed)		# Internal representation, don't use outside


	def __init__(self, COM='sep', baudrate=115200):
		# Simulates incorrect port
		# Correct port is 'sep'
		if COM != 'sep':
			return

		self.connected = True
		self.timer = Timer(TRANSITION_DURATION, self.transitionTimer)


	def initTimer(self):
		self.timer.cancel()		# Cancel previous call
		self.timer = Timer(TRANSITION_DURATION, self.transitionTimer)
		self.timer.setDaemon(True)
		self.timer.start()

	def transitionTimer(self):
		if self.gate.state not in [GS.Opening, GS.Closing]:
			return

		# Simulates an error
		if int(time.time()) % 10  == 2:
			self.gate.setState(GS.Error)

		else:
			if self.gate.state == GS.Opening:
				self.gate.setState( GS.Opened )
			if self.gate.state == GS.Closing:
				self.gate.setState( GS.Closed )

	def sendMsg(self, msg):
		if msg == '0':
			self.sendSignal()

	def sendSignal(self):
		sg = self.gate

		# Abrir si esta cerrado
		if sg.state == GS.Closed:
			sg.setState( GS.Opening )

		# Cerrar si esta abierto
		elif sg.state == GS.Opened:
			sg.setState( GS.Closing )

		# Si esta detenido, moverse en sentido opuesto a lo anterior
		elif sg.state == GS.Stopped:
			# Si estaba abriendose, ahora se cierra
			if sg.prev_state == GS.Opening:
				sg.setState( GS.Closing )
			# Si estaba cerrandose o hubo error, ahora se abre
			else:
				sg.setState( GS.Opening )

		# Si se esta abriendo o cerrando, detener
		elif sg.state in [GS.Opening, GS.Closing]:
			sg.setState( GS.Stopped )

		elif sg.state == GS.Error:
			sg.setState( GS.Closing )
			sg.setState( GS.Stopped )

		self.initTimer()

		#last_signal_time = time.time()
		return True


	def requestState(self, asString=False):
		if asString:
			return GS.ToString(self.gate.state)
		else:
			return self.gate.state
		


# --------------- Testing -------------------------

if __name__ == '__main__':
	a = uC_interface()
	print 'Connected:', a.connected
	print 'State', a.requestState(True)

	for i in range(2):
		print 'Signal', a.sendSignal()
		print 'State', a.requestState(True)

		for i in range(3):
			time.sleep(1)
			print 'State', a.requestState(True)

	for i in range(2):
		print 'Signal', a.sendSignal()
		print 'State', a.requestState(True)
		time.sleep(1)

