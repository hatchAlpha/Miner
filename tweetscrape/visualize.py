from http.server import BaseHTTPRequestHandler
from socketserver import TCPServer
from stream import path
import vincent

def vis(data_set,cat,port):
	donut=vincent.Pie(data_set[cat],inner_radius=150)
	donut.colors(brew='Set2')
	donut.legend(cat)
	
	class Handler(BaseHTTPRequestHandler):
		def handle_one_request(self):
			data=open(path+'/http/index.html','r').read()

			self.wfile.write(bytes(data.replace('{{spec}}',donut.to_json()),encoding='utf-8'))

	try:
		print("Serving visualization on 127.0.0.1:"+str(port))

		httpd=TCPServer(('',port),Handler)
		httpd.serve_forever()
	except KeyboardInterrupt:
		exit()