from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def this_is_test() -> dict[str, str]:
    return {'message': 'Olá, Inácio'}
