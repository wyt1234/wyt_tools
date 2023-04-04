import uvicorn
from fastapi import FastAPI, File
from io import BytesIO
import pandas as pd

app = FastAPI()


@app.post("/files/")
def read_item(file1: bytes = File(), file2: bytes = File()):
    df = pd.read_csv(BytesIO(file1))
    df2 = pd.read_csv(BytesIO(file2))
    print(df)
    print(df2)


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
