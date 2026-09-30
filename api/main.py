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

def criar_tabela():
    conexao = conectar_banco()

    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leituras (
            id SERIAL PRIMARY KEY,
            temperatura REAL NOT NULL,
            umidade_ar REAL NOT NULL,
            umidade_solo INTEGER NOT NULL,
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conexao.commit()

    cursor.close()
    conexao.close()

criar_tabela()

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

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO leituras (
            temperatura,
            umidade_ar,
            umidade_solo
        )
        VALUES (%s, %s, %s)
    """, (
        dados.temperatura,
        dados.umidade_ar,
        dados.umidade_solo
    ))

    conexao.commit()

    cursor.close()
    conexao.close()

    return {
        "status": "ok",
        "mensagem": "Dados recebidos com sucesso"
    }