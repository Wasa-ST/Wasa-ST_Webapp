from fastapi import APIRouter, Request,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm

from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from .utils import is_active,templates
from .security import get_current_user,oauth2_scheme,create_access_token,create_refresh_token

from .models import User,UserCreate
from .database import users_db

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    token = request.cookies.get("access_token")
    if token:

        try:
            user = get_current_user(token)
            


            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "is_active": is_active,
                    "user_role": user.get("role"),
                    "username": user.get("username"),
                },
            )

        except Exception as e:

            return templates.TemplateResponse(
                "login.html",
                {"request": request, "user_role": None, "is_active": is_active},
            )

    return templates.TemplateResponse(
        "login.html", {"request": request, "user_role": None, "is_active": is_active}
    )


@router.post("/token")
def login(
    request: Request, form_data: OAuth2PasswordRequestForm = Depends()
):  # Added request parameter
    user = users_db.get(form_data.username)

    if not user or user["password"] != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]}
    )
    refresh_token = create_refresh_token(
        data={"sub": user["username"], "role": user["role"]}
    )
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=access_token, httponly=True, path="/")
    response.set_cookie(
        key="refresh_token", value=refresh_token, httponly=True, path="/"
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/login")
async def login_page(request: Request):

    token = request.cookies.get("access_token")
    

    if token:
        print(get_current_user(token))
        try:
            user = get_current_user(token)

            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "is_active": is_active,
                    "user_role": user.get("role"),
                },
            )

        except Exception as e:

            return templates.TemplateResponse(
                "login.html",
                {"request": request, "user_role": None, "is_active": is_active},
            )

    return templates.TemplateResponse(
        "login.html",
        {"request": request, "user_role": None, "is_active": is_active},
    )


@router.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return response


@router.get("/create_hr_user", response_class=HTMLResponse)
async def create_hr_user(request: Request):

    token = request.cookies.get("access_token")
    token_data = get_current_user(token)

    if token_data["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
        )
    return templates.TemplateResponse(
        "create_hr_user.html",
        {"request": request, "user_role": "admin", "is_active": is_active},
    )


@router.post("/post_create-hr-user/")
def post_create_hr_user(user: UserCreate, token: str = Depends(oauth2_scheme)):
    token_data = get_current_user(token)

    if user.username in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )
    users_db[user.username] = {
        "username": user.username,
        "password": user.password,
        "role": user.role,
    }
    return {"msg": "User created successfully"}