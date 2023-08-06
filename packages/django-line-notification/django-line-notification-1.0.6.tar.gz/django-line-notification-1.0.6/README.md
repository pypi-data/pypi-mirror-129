In group chat must has line bot notify included.


Code example.

from django_line_notification.line_notify import LINE

token = 'oiojweifIedDN0209%dp9icdfgergIJiw672gcu7wiu'

line = Line(token)

line.send_msg('foobar')

