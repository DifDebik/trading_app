from fastapi import FastAPI

app = FastAPI(
    title='Trading App'
)


@app.get('/')
def get_hello():
    return 'Hello, World!'
