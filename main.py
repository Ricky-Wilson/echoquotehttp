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
CRLF = '\r\n'
SP = ' '
CR = '\r'
HOST = 'www.example.com'
PORT = 80
PATH = '/'


def request_header(host=HOST, path=PATH):
    """
    Create a request header.
    """
    return CRLF.join([
        "GET {} HTTP/1.1".format(path), "Host: {}".format(host),
        "Connection: Close\r\n\r\n"
    ])


def parse_header(header):
    # The response-header fields allow the server 
    # to pass additional information about the 
    # response which cannot be placed in the 
    # Status- Line. 
    
    # These header fields give information about 
    # the server and about further access to the 
    # resource identified by the Request-URI.
    header_fields = header.split(CR)
    # The first line of a Response message is the 
    # Status-Line, consisting of the protocol version 
    # followed by a numeric status code and its 
    # associated textual phrase, with each element 
    # separated by SP characters.

    # Get the numeric status code from the status
    # line.
    code = header_fields.pop(0).split(' ')[1]
    header = {}
    for field in header_fields:
        key, value = field.split(':', 1)
        header[key.lower()] = value
    return header, code


def send_request(host=HOST, path=PATH, port=PORT):
    """
    Send an HTTP GET request.
    """

    # Create the socket object.
    """
    A network socket is an internal endpoint 
    for sending or receiving data within a node on 
    a computer network.

    Concretely, it is a representation of this 
    endpoint in networking software (protocol stack), 
    such as an entry in a table 
    (listing communication protocol, 
    destination, status, etc.), and is a form of 
    system resource.

    The term socket is analogous to physical 
    female connectors, communication between two 
    nodes through a channel being visualized as a 
    cable with two male connectors plugging into 
    sockets at each node. 
    
    Similarly, the term port (another term for a female connector) 
    is used for external endpoints at a node, 
    and the term socket is also used for an 
    internal endpoint of local inter-process 
    communication (IPC) (not over a network). 
    However, the analogy is limited, as network 
    communication need not be one-to-one or 
    have a dedicated communication channel.
    """
    sock = socket.socket()
    # Connect to the server.
    sock.connect((host, port))
    # Send the request.
    sock.send(request_header(host, path))

    # Get the response.
    response = ''
    chuncks = sock.recv(4096)
    while chuncks:
        response += chuncks
        chuncks = sock.recv(4096)

    # HTTP headers will be separated from the body by an empty line
    header, _, body = response.partition(CRLF + CRLF)
    header, code = parse_header(header)
    return header, code, body


header, code, body  = send_request(host='www.google.com')
print code, CRLF, body