from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "from BetOS!"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("user/new")
def new_user(
    username: str, first_name: str, last_name: str, email: str, cpf_cnpj: str, password
):
    return {"Username:": username}


@app.post("user/login")
def login(username: str, password: str):
    return {"username:": username}
