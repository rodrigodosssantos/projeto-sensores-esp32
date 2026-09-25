from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class DadosSensores(BaseModel):
    temperatura: float
    umidade_ar: float
    umidade_solo: int


@app.get("/")
def inicio():
    return {
        "mensagem": "API dos sensores funcionando!"
    }


@app.post("/dados")
def receber_dados(dados: DadosSensores):

    print("Dados recebidos:")
    print(f"Temperatura: {dados.temperatura} °C")
    print(f"Umidade do ar: {dados.umidade_ar} %")
    print(f"Umidade do solo: {dados.umidade_solo} %")

    return {
        "status": "ok",
        "mensagem": "Dados recebidos com sucesso"
    }