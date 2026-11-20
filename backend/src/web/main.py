from fastapi import FastAPI

from web.controllers import conversation_controller

app = FastAPI()
app.include_router(conversation_controller.router)


@app.get("/health")
def health():
    return {"status": "ok"}
