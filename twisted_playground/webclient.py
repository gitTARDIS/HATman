from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from config import port;

class Greeter(Protocol):
	def sendMessage(self, msg):
		self.transport.write("MESSAGE %s\n" % msg)

def gotProtocol(p):
	p.sendMessage("Hello")
	reactor.callLater(1, p.sendMessage, "This is sent in a second")
	reactor.callLater(2, p.transport.loseConnection)

point = TCP4ClientEndpoint(reactor, "localhost", port)
d = connectProtocol(point, Greeter())
d.addCallback(gotProtocol)
reactor.run()