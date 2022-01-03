from enum import Enum


class ContentType(Enum):
    html = "text/html; charset=utf-8"
    htm = "text/html; charset=utf-8"
    txt = "text/html; charset=utf-8"
    text = "text/html; charset=utf-8"
    js = "text/javascript; charset=utf-8"
    css = "text/css"
    jpg = "image/jpeg"
    ico = "image/vnd.microsoft.icon"
    gif = "image/gif"
    json = "application/json"
    xml = "application/xml"

    def __str__(self):
        return "content-type: " + self.value
