from twisted.web import server, resource
from twisted.internet import reactor, endpoints

# -------------------------------------
# config
# -------------------------------------

protocol = "tcp";
port = "8080";

# ------------------------------------


print("INFO Server running on port " + port);

class Counter(resource.Resource):
	isLeaf = True
	numberRequests = 0

	def render_GET(self, request):
		print("INFO Server got a request");
		self.numberRequests += 1
		request.setHeader(b"content-type", b"text/plain")
		content = u"I am request #{}\n".format(self.numberRequests)
		return content.encode("ascii")

endpoints.serverFromString(reactor, protocol + ":" + port).listen(server.Site(Counter()))
reactor.run()