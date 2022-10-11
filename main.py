import uvicorn
from fastapi import FastAPI

from model import webcam_capture

app = FastAPI()

# Index route, opens automatically on the port route 8000
@app.get("/")
def index():
    return {"Hello": "Sheilah"}


@app.post("/predict")
def get_prediction():
    return webcam_capture
    

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)
