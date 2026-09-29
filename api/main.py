from fastapi import FastAPI
from pydantic import BaseModel
import os
import psycopg


DATABASE_URL = os.getenv("DATABASE_URL")

print("DATABASE_URL configurada:", DATABASE_URL is not None)

app = FastAPI()


class DadosSensores(BaseModel):
    temperatura: float
    umidade_ar: float
    umidade_solo: int


def conectar_banco():
    return psycopg.connect(DATABASE_URL)


@app.get("/")
def inicio():
    return {
        "mensagem": "API dos sensores funcionando!"
    }


@app.get("/teste-banco")
def teste_banco():

    try:
        conexao = conectar_banco()
        conexao.close()

        return {
            "status": "ok",
            "mensagem": "Conexao com o banco funcionando!"
        }

    except Exception as erro:

        return {
            "status": "erro",
            "mensagem": str(erro)
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