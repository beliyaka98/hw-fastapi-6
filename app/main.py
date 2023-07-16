from fastapi import Cookie, FastAPI, Form, Request, Response, templating
from fastapi.responses import RedirectResponse

from .flowers_repository import Flower, FlowersRepository
from .purchases_repository import Purchase, PurchasesRepository
from .users_repository import User, UsersRepository

from typing import List
from jose import jwt
import json
app = FastAPI()
templates = templating.Jinja2Templates("templates")


flowers_repository = FlowersRepository()
purchases_repository = PurchasesRepository()
users_repository = UsersRepository() 

def create_jwt(user_id: int) -> str:
    body = {"user_id": user_id}
    token = jwt.encode(body, "TorTokaeva", "HS256")
    return token

def decode_jwt(token: str) -> int:
    data = jwt.decode(token, "TorTokaeva", "HS256")
    return data["user_id"]

@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/signup")
def get_signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
def post_signup(request: Request,
                email: str = Form(),
                full_name: str = Form(),
                password: str = Form()):
    users_repository.signup(email, full_name, password)
    return RedirectResponse("/login", status_code=303)

@app.get("/login")
def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def get_login(
    request: Request,
    email: str = Form(),
    password: str = Form()
):
    
    user = users_repository.get_user_by_email(email)
    if not user or user.password != password:
        return RedirectResponse("/login", status_code=303)
    
    response = RedirectResponse("/profile", status_code=303)
    token = create_jwt(user.id)
    response.set_cookie("token", token)
    return response

@app.get("/profile")
def get_profile(
    request: Request,
    token: str = Cookie()
):
    user_id = decode_jwt(token)
    user = users_repository.get_user_by_id(user_id)
    return templates.TemplateResponse("profile.html", {"request": request, "user": user})


@app.get("/flowers")
def get_flowers(request: Request):
    return templates.TemplateResponse(
        "flowers.html", 
        {"request": request, "flowers": flowers_repository.flowers})

@app.post("/flowers")
def post_flowers(
    request: Request,
    name: str = Form(),
    count: int = Form(),
    cost: int = Form()
):
    flowers_repository.add_flower(name, count, cost)
    return RedirectResponse("/flowers", status_code=303)

@app.post("/cart/items")
def post_cart_items(
    request: Request,
    flower_id: int = Form(),
    cart_items: str = Cookie(default="[]"),
):
    cart_items = json.loads(cart_items)
    cart_items.append(flower_id)
    print(cart_items)
    cart_items = json.dumps(cart_items)
    response = RedirectResponse("/flowers", status_code=303)
    response.set_cookie(key="cart_items", value=cart_items)
    return response

@app.get("/cart/items")
def get_cart_items(
    request: Request,
    cart_items: str = Cookie(default="[]"),
):
    cart_items = json.loads(cart_items)
    flowers = [flower for flower in flowers_repository.flowers if flower.id in cart_items]
    total_cost = sum(flower.cost for flower in flowers)
    return templates.TemplateResponse(
        "carts.html",
        {
            "request": request,
            "flowers": flowers,
            "total_cost": total_cost
        })