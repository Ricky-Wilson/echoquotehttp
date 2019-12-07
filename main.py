"""
This module is a demonstration of how to send
a HTTP request from scratch with the socket module.
"""

__author__ = "Ricky L Wilson."
__email__ = "echoquote@gmail.com"

import socket


"""
The term CRLF refers to Carriage Return (ASCII 13, \r)
Line Feed (ASCII 10, \n).
They're used to note the termination of a line,
however, dealt with
differently in today's popular Operating Systems.
"""
CRLF = "\r\n"
HOST = "www.example.com"
PORT = 80
PATH = "/"


def request_header(host=HOST, path=PATH):
    """
    Create the request header.
    """
    return CRLF.join([
      "GET {} HTTP/1.1".format(path),
      "Host: {}".format(host),
      "Connection: Close\r\n\r\n"])

def send_request(host=HOST, path=PATH, port=PORT):
    request = request_header(host, path)
    print request

    # Connect to the server
    s = socket.socket()
    s.connect((host, PORT))

    # Send an HTTP request
    s.send(request)

    # Get the response (in several parts, if necessary)
    response = ''
    chuncks = s.recv(4096)
    while chuncks:
        response += chuncks
        chuncks = s.recv(4096)

    # HTTP headers will be separated from the body by an empty line
    header_data, _, body = response.partition(CRLF + CRLF)
    print(header_data)
    print(body)