from fastapi import Request
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")

# active highlight link function
def is_active(request: Request, link: str) -> str:
    return "active" if request.url.path == link else ""
