
"""
This module is a demonstration of how to send
a HTTP request from scratch with the socket module.
"""
import socket

__author__ = "Ricky L Wilson."
__email__ = "echoquote@gmail.com"
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
        "GET {} HTTP/1.1".format(path), "Host: {}".format(host),
        "Connection: Close\r\n\r\n"
    ])


def parse_header(header):
    values = header.split('\r')
    code = values.pop(0).split(' ')[1]
    header = {}
    for line in values:
        k, v = line.split(':', 1)
        header[k.lower()] = v
    return header, code


def send_request(host=HOST, path=PATH, port=PORT):
    """
    Send an HTTP GET request.
    """

    # Connect to the server and send the request.
    sock = socket.socket()
    sock.connect((host, port))
    sock.send(request_header(host, path))

    # Get the response (in several parts, if necessary)
    response = ''
    chuncks = sock.recv(4096)
    while chuncks:
        response += chuncks
        chuncks = sock.recv(4096)

    # HTTP headers will be separated from the body by an empty line
    header, _, body = response.partition(CRLF + CRLF)
    header, code = parse_header(header)
    return header, code, body


print send_request()[1]
