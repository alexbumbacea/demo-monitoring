from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import socket
import platform
import random

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP


class S(BaseHTTPRequestHandler):
    def _set_response(self, method):
        data = "working_time#method={0},lang={1},langVersion={2}:{3}|ms".format(method, "python",
                                                                                platform.python_version(),
                                                                                random.randint(50, 90000) * 1000)

        self.send_response(200)
        self.send_header('Stats', data)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        sock.sendto(
            data.encode("utf-8"),
            ('statsd-exporter', 9125)
        )

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response("GET")
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        # content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        # post_data = self.rfile.read(content_length) # <--- Gets the data itself
        # logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
        #              str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response("POST")
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))


def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
