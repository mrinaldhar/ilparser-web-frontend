import json
import sys
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import multiprocessing as mp
import urllib
import cgi
import urllib2
import re
import requests

data = []
keywordIndex = {}
smalldata = []
reload(sys)
sys.setdefaultencoding('utf-8')


'''
Handler for the integrated web server interface
'''
class S(BaseHTTPRequestHandler):
	def _set_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.send_header('Access-Control-Allow-Origin', '*')
		self.end_headers()


	'''
	Handles GET requests for the server
	'''
	def do_GET(self):
		self._set_headers()
		args = {}
		idx = self.path.find('?')
		if idx >= 0:
			rpath = self.path[:idx]
			args = cgi.parse_qs(self.path[idx+1:])
		else:
			rpath = self.path

		if rpath == '/parse':
			data = args.get("data", 0)[0]
			lang = args.get("lang", 0)[0]
			print data, lang
			r = requests.post("http://localhost:3000/parse/"+lang, data={'data': data})		
			self.wfile.write(r.text)
		else:															# Request for all other files
			self.wfile.write("Something went wrong!")

	def do_HEAD(self):
		self._set_headers()
		
	def do_POST(self):
		# Doesn't do anything with posted data
		self._set_headers()
		self.wfile.write("<html><body><h1>POST requests are not needed for this service!</h1></body></html>")
		
'''
Starts the HTTP server
'''
def run_server(server_class=HTTPServer, handler_class=S, port=5005):
	server_address = ('0.0.0.0', port)
	httpd = server_class(server_address, handler_class)
	print 'Starting httpd...'
	httpd.serve_forever()




def init():
	c = mp.Process(target=run_server)				# HTTP server process
	c.start()

if __name__ == "__main__":
	init()
