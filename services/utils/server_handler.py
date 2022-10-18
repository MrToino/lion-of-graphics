from http.server import SimpleHTTPRequestHandler, HTTPServer
from requests_toolbelt.multipart import decoder
from socketserver import ThreadingMixIn


class MPBRequestHandler(SimpleHTTPRequestHandler):
    def _set_headers(self, content_length: int = 0) -> None:
        """Sets the response headers for the give content_length"""
        self.send_header('Content-Type', 'text/plain')
        self.send_header("Content-Length", str(content_length))
        self.end_headers()

    def _return_400(self, message: str = "Bad Request") -> None:
        """Sends a response with status code 400 - Bad Request"""
        self.send_response(400)
        self._set_headers(len(message))
        self.wfile.write(message.encode())

    def _return_405(self, message: str = "Method Not Allowed") -> None:
        """Sends a response with status code 405 - Method Not Allowed"""
        self.send_response(405)
        self._set_headers(len(message))
        self.wfile.write(message.encode())

    def _return_500(self, message: str = "Internal Server Error") -> None:
        """Sends a response with status code 500 - Internal Server Error"""
        self.send_response(500)
        self._set_headers(len(message))
        self.wfile.write(message.encode())

    """Define the default answer for all methods"""
    do_GET = _return_405
    do_HEAD = _return_405
    do_POST = _return_405
    do_PUT = _return_405
    do_DELETE = _return_405
    do_CONNECT = _return_405
    do_OPTIONS = _return_405
    do_TRACE = _return_405
    do_PATCH = _return_405

    def _multipart_parser(self, request: bytes) -> tuple:
        """Parses multipart request into parts"""
        message = decoder.MultipartDecoder(request, self.headers.get("content-type"))
        return message.parts


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle http requests in a separate thread."""
