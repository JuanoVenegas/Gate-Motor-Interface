"""Subclass of GateMotorInterfaceFrame, which is generated by wxFormBuilder."""

import os
import sys
import time
import platform
import wx
import GateMotorInterface
import gate as g

simulation = True

if simulation:
	import uC_simulation as uClib	
else:
	import uC_interface as uClib



# ----- Util functions ---------------------------------------------------------
def isLinux():
	return 'Linux' in platform.system()

# Find an element in an object. Print list with string matches.
def find(st, obj):
	print(filter(lambda x: st in x, dir(obj)))


# ----- Main functions ---------------------------------------------------------
class GMI( GateMotorInterface.GateMotorInterfaceFrame ):
	def __init__( self, parent ):
		GateMotorInterface.GateMotorInterfaceFrame.__init__( self, parent )

		# Init
		# Main window processes key events first
		self.Bind(wx.EVT_CHAR_HOOK, self.OnKeyDown)

		# Configure console
		self.m_textCtrl_console.SetFont( wx.Font( 11, 76, 90, 90, False, "Ubuntu Mono" ) )
		self.m_textCtrl_consoleInput.SetFont( wx.Font( 11, 76, 90, 90, False, "Ubuntu Mono" ) )

		# Gate state variables
		self.gate = g.Gate(g.GateStates.Closed)

		# Image animation variables
		self.gate_closed_position = 230
		self.gate_opened_position = 440
		self.gate_middle_position = 320
		self.gate_image_pos = self.gate_image.GetPosition()
		self.animation_timer = wx.Timer()
		self.animation_timer.Bind(wx.EVT_TIMER, self.animateGate)
		self.animation_timer.Start(10)
		
		# Indicator
		#self.stateTransitionLabel()

		# Change serial port text
		if isLinux():
			self.m_textCtrl_COM.Value = '/dev/ttyACM0'
		self.m_textCtrl_COM.SetFocus()

		# Micro controller
		self.uC = None

		# Auto request timer
		self.request_timer = wx.Timer()
		self.request_timer.Bind(wx.EVT_TIMER, self.autoRequest)
		self.request_timer.Start(100)



	def OnKeyDown( self, event ):
		if event.GetKeyCode() == wx.WXK_ESCAPE:		# Salir con tecla Escape
			self.Close()
		elif event.GetKeyCode() == wx.WXK_TAB:		# Cambo de modo
			# TEST
			self.SendSignal(None)
			#self.stateTransitionLabel()
		else:
			event.Skip()



	def sendCommand( self, event ):
		cmd = self.m_textCtrl_consoleInput.Value
		if self.uC is not None and self.uC.connected:
			self.uC.sendMsg(cmd)
			self.appendTerminal('>> ' + cmd)
		else:
			self.appendTerminal('>> uController not connected !')


	def appendTerminal(self, s):
		print(s)
		self.m_textCtrl_console.Value += '\n' + s


	def stateTransitionLabel(self):
		#self.m_staticText_opening.Hide()
		#self.m_staticText_closing.Hide()
		#self.m_staticText_stopped.Hide()

		if self.gate.state == g.GateStates.Opening:
			self.m_staticText_opening.Show()
			self.m_staticText_closing.Hide()
			self.m_staticText_stopped.Hide()
		if self.gate.state == g.GateStates.Closing:
			self.m_staticText_opening.Hide()
			self.m_staticText_closing.Show()
			self.m_staticText_stopped.Hide()
		if self.gate.state in [g.GateStates.Opened, g.GateStates.Closed, g.GateStates.Stopped, g.GateStates.Error]:
			self.m_staticText_opening.Hide()
			self.m_staticText_closing.Hide()			
			self.m_staticText_stopped.Show()
			self.m_staticText_stopped.SetLabel(('--%s--'%g.GateStates.ToString(self.gate.state)).upper())

		#self.m_panel_labelState.Layout()
		self.bSizer_stateLabel.Layout()
	

	def animateGate(self, event):
		self.stateTransitionLabel()

		if self.uC is None:
			self.gate_image.SetPosition( [self.gate_closed_position, self.gate_image.GetPosition()[1]] )
			return

		if self.gate.state == g.GateStates.Stopped:
			return

		setPoint = self.gate_middle_position
		if self.gate.state == g.GateStates.Opened:
			setPoint = self.gate_opened_position
		if self.gate.state == g.GateStates.Closed:
			setPoint = self.gate_closed_position

		if self.gate.state == g.GateStates.Opening:
			setPoint = int(0.25*self.gate_closed_position + 0.75*self.gate_opened_position)
		if self.gate.state == g.GateStates.Closing:
			setPoint = int(0.75*self.gate_closed_position + 0.25*self.gate_opened_position)

		px, py = self.gate_image.GetPosition()
		if px > setPoint:
			px -= 1
		if px < setPoint:
			px += 1

		self.gate_image.SetPosition( [px,py] )
	

	def Connect_uC(self, event):
		if self.uC is None or not self.uC.connected:
			self.uC = uClib.uC_interface( self.m_textCtrl_COM.Value )
			if self.uC.connected:
				self.m_checkBox_connected.Value = True
				self.appendTerminal('<< CONNECTED')
			else:
				self.appendTerminal('<< Connection Failed !')
		elif self.uC.connected:
			self.appendTerminal('<< already connected')


	def SendSignal(self, event):
		if self.uC is not None and self.uC.connected:
			self.uC.sendSignal()
			self.appendTerminal('>> signal sent')
		else:
			self.appendTerminal('>> uController not connected !')

	def RequestStatus(self, event, printAlways=True):
		if self.uC is not None and self.uC.connected:
			s = self.uC.requestState()
			doPrint = printAlways or self.gate.state != s
			self.gate.setState( s )
			if doPrint:
				self.appendTerminal('<< status: ' + g.GateStates.ToString(s))
		elif printAlways:
			self.appendTerminal('<< uController not connected !')


	def autoRequest(self, event):
		if self.m_checkBoxAutoRequest.Value:
			self.RequestStatus(None, False)




if __name__ == "__main__":
	app = wx.App(False)
	frame = GMI(None)
	frame.Show(True)
	app.MainLoop()
