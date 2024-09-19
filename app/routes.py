from fastapi import APIRouter, Request, Depends,Form, HTTPException, status
from typing import Dict
from fastapi.security import OAuth2PasswordRequestForm

from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from .utils import is_active, templates
from .security import (
    get_current_user,
    oauth2_scheme,
    create_access_token,
    create_refresh_token,
)

from .models import User, UserCreate
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
                    "user_type": user.get("user_type"),
                    "username": user.get("username"),
                },
            )

        except Exception as e:

            return templates.TemplateResponse(
                "login.html",
                {"request": request, "user_type": None, "is_active": is_active},
            )

    return templates.TemplateResponse(
        "login.html", {"request": request, "user_type": None, "is_active": is_active}
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
        data={"sub": user["username"], "user_type": user["user_type"]}
    )
    refresh_token = create_refresh_token(
        data={"sub": user["username"], "user_type": user["user_type"]}
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
        try:
            user = get_current_user(token)

            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "is_active": is_active,
                    "user_type": user.get("user_type"),
                },
            )

        except Exception as e:

            return templates.TemplateResponse(
                "login.html",
                {"request": request, "user_type": None, "is_active": is_active},
            )

    return templates.TemplateResponse(
        "login.html",
        {"request": request, "user_type": None, "is_active": is_active},
    )


@router.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return response


@router.get("/create_user", response_class=HTMLResponse)
async def create_user(request: Request):

    token = request.cookies.get("access_token")
    token_data = get_current_user(token)

    if token_data["user_type"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
        )
    return templates.TemplateResponse(
        "create_user.html",
        {
            "request": request,
            "user_type": token_data.get("user_type"),
            "is_active": is_active,
        },
    )




@router.get("/show_users", response_class=HTMLResponse)
async def show_users(request: Request):

    
    token = request.cookies.get("access_token")
    token_data = get_current_user(token)

    

    if token_data["user_type"] not in ["admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
        )
    



    
    
    return templates.TemplateResponse(
        "show_users.html",
        {
            "request": request,
            "user_type": token_data.get("user_type"),
            "is_active": is_active,
            "db":users_db
        },
    )



@router.post("/post_create-user/")
def post_create_user(user: UserCreate, token: str = Depends(oauth2_scheme)):
    token_data = get_current_user(token)

    if user.username in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )
    

    users_db[user.username] = {
        "username": user.username,
        "name": user.name,
        "password": user.password,
        "user_type": user.user_type,
        "designation": user.designation,
        "ticket_no": user.ticket_no,
        "ward": user.ward,
        "place_of_posting": user.place_of_posting,

        
    }
    return {"msg": "User created successfully"}


@router.get("/edit_users/")
async def edit_users(request: Request):
    username = request.query_params.get('username')
    user_data = users_db.get(username, {})

    token = request.cookies.get("access_token")
    if token:
        

        return templates.TemplateResponse(
            "edit_users.html",
            {
                "request": request,
                "user_data": user_data,  
                "is_active": is_active,
                "user_type":get_current_user(token).get("user_type")
            },
        )

@router.post("/post_edit_users/")
async def post_edit_users(data: Dict[str, str], request: Request):
    select_username = data.get("username")
    token = data.get("token")
    current_user = get_current_user(token).get("user_type")

    return JSONResponse(content={"redirect_url": "/edit_users", "username": select_username})




@router.get("/post_user/")
async def post_user(request: Request):
    username = request.query_params.get('username')
    user_data = users_db.get(username, {})

    token = request.cookies.get("access_token")
    if token:
        

        return templates.TemplateResponse(
            "edit_users",
            {
                "request": request,
                "user_data": user_data,  
                "is_active": is_active,
                "user_type":get_current_user(token).get("user_type")
            },
        )


@router.post("/post_update_users/")
async def post_update_users(data: Dict[str, str], request: Request):

    select_username = data.get("username")
    token = data.get("token")
    current_user = get_current_user(token).get("user_type")

    if current_user == "admin":
       for k,v in data.items():
        if k not in ['username','token']:
            users_db.get(select_username)[k] = v
        

    return JSONResponse(content={"redirect_url": "/post_user", "username": select_username}) 

    # return JSONResponse(content={"redirect_url": "/edit_users", "username": select_username})
