## Prerequisite

- Group chat with Line bot included.

## Code example.

```python
from django_line_notification.line_notify import Line

token = 'oiojweifIedDN0209%dp9icdfgergIJiw672gcu7wiu'
line = Line(token)
line.send_msg('foobar')
```



