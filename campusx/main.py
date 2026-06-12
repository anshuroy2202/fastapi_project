from fastapi import FastAPI

app=FastAPI()

@app.get("/") #("end point")
def start():
    return { "message":"You are WELCOME!!"}


@app.get("/info")
def information():
    return {
        "name":"Roy",
        "occupation":"Bussinessman",
        "net-worth":"100 Billions",
        "youtube":"campusx"
    }