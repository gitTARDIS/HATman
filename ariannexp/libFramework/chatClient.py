import pyarianne
import curses
import curses.ascii
import os
import time
import signal
import sys


def sendMessage(lines):
	text = ""
	for i in lines:
		text = text + i + "\n"
	action=pyarianne.RPAction()
	action.put("type","chat")
	action.put("content",text)
	pyarianne.send(action)
	

def paintStatusArea(text):
	statusArea.clear()
	statusArea.border()
	statusArea.addstr(1,1,text,curses.color_pair(3))
	statusArea.refresh()

def paintTextArea(history_lines):
	textArea.clear()
	textArea.border()
	textArea.addstr(0,3," The first marauroa-python-curses-chat client ")
	row=1
	color_name = 1
	color_text = 2
	for line_entry in history_lines:
		name = line_entry['name']
		text = line_entry['text']
		if name == my_name:
			color_name = 5
		else:
			color_name = 1
		if text.find(my_name) != -1:
			color_text = 6
		else:
			color_text = 2
			name = name.rjust(16)+": "
			textArea.addstr(row,1,name,curses.color_pair(color_name))
			textArea.addstr(text,curses.color_pair(color_text))
			row=row+1
	textArea.refresh()

def paintInputArea(text):
	inputArea.clear()
	inputArea.border()
	inputArea.addstr(0,4,time.strftime(" %d.%m.%Y %H:%M:%S "), curses.color_pair(1))
	inputArea.addstr(1,1,">"+text)
	inputArea.refresh()
	
def repaintInputArea():
	global text
	paintInputArea(text)

def dostuffonCallback():	
	if False:
		 paintStatusArea("Calling from Python!")
	return 1

def printChatMessage(world):
	global history_lines
	if True:
		for i in world.objects:		 
			if world.objects[i].get("type") == "character":
				name = world.objects[i].get("name")
			if world.objects[i].has("?text"):			 
				text = world.objects[i].get("?text")
				text_lines = text.split("\n")
			for line in text_lines:
				if line != "":
					history_lines.append({'name': name,'text': line})

			#if overflow - remove first element
			while len(history_lines) > 18: 
				history_lines.pop(0)

			paintTextArea(history_lines)
			repaintInputArea()


def initCurses():
	stdscr = curses.initscr()
	curses.noecho()
	curses.cbreak()
	stdscr.keypad(True)
	stdscr.nodelay(True)
	if curses.has_colors():
		curses.start_color()
		curses.init_pair(1, curses.COLOR_BLUE,	 curses.COLOR_BLACK);
		curses.init_pair(2, curses.COLOR_GREEN,	curses.COLOR_BLACK);
		curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK);
		curses.init_pair(4, curses.COLOR_RED,	curses.COLOR_BLACK);
		curses.init_pair(5, curses.COLOR_CYAN,	 curses.COLOR_BLACK);
		curses.init_pair(6, curses.COLOR_MAGENTA,curses.COLOR_BLACK);
		curses.init_pair(7, curses.COLOR_WHITE,	curses.COLOR_BLACK);
	return stdscr

def uninitCurses(sign,arg2):
	signal.signal(sign, signal.SIG_IGN)
	try:
		curses.nocbreak()
		stdscr.keypad(0)
		stdscr.nodelay(0)
		curses.echo()
		curses.endwin()
		#print "Exiting by signal "+ str(sign)
	except err:
		print ("Exception: " +str(err))
	sys.exit(0)

def logout():
	paintStatusArea("Logging out...")
	pyarianne.logout()
	paintStatusArea("Logged out.")

def exit(arg1,arg2):
	logout()
	uninitCurses(arg1,arg2)	

stdscr = initCurses()

#register singal handler to be able to restore the console
signal.signal(signal.SIGINT,	exit) #ctrl-c
signal.signal(signal.SIGTERM, exit) 

begin_x = 0 ; begin_y = 0
height	= 20 ; width = 100
textArea = curses.newwin(height, width, begin_y, begin_x)

begin_x = 0 ; begin_y = 20
height	= 3 ; width = 100
inputArea = curses.newwin(height, width, begin_y, begin_x)
inputArea.keypad(True)
inputArea.nodelay(True)


begin_x = 0 ; begin_y = 23
height	= 3 ; width = 100
statusArea = curses.newwin(height, width, begin_y, begin_x)

host = "marauroa.ath.cx"
port = 3214
my_name = "root777"
pwd	= "root777"

world=pyarianne.World()
perceptionHandler=pyarianne.PerceptionHandler()
pyarianne.setIdleMethod(dostuffonCallback)
pyarianne.connectToArianne(host,port)
paintStatusArea("Connecting to server "+host+":"+str(port)+"...")
text = ""
history_lines = [{'name': my_name, 'text': "<entered>"}]
if pyarianne.login(my_name,pwd):
	chars=pyarianne.availableCharacters()
	paintStatusArea("Logged in, choosing character "+chars[0]+"...")
	if pyarianne.chooseCharacter(chars[0]):
		paintStatusArea("Choosed character "+chars[0])
		exit = False
	paintTextArea(history_lines)
	repaintInputArea()
	while True:
		time.sleep(0.1)
		if pyarianne.hasPerception():
			perception=pyarianne.getPerception()
			perceptionHandler.applyPerception(perception, world)
		printChatMessage(world)

		ch = inputArea.getch()
		if ch != curses.ERR :			 
			if ch == 10 or ch == curses.KEY_ENTER: #enter
				if text == "/quit":
					break
				if text != "":
					sendMessage([text])
					text = ""
					repaintInputArea()
				elif ch == curses.ascii.DEL:
					text=text[:-1]
					repaintInputArea()
				elif curses.ascii.isprint(ch):			 
					text = text + chr(ch) 			
					repaintInputArea()
				else:
					paintStatusArea("Unhandled key "+str(ch))
					logout()
			else:
				paintStatusArea("CAN'T CHOOSE: "+pyarianne.errorReason())
		else:
			paintStatusArea("CAN'T LOGIN: "+pyarianne.errorReason())

paintStatusArea("Finishing pyclient")
uninitCurses(1,2)
