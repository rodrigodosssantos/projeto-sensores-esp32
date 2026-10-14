
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import psycopg


DATABASE_URL = os.getenv("DATABASE_URL")

print("DATABASE_URL configurada:", DATABASE_URL is not None)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Para testes; restrinja ao domínio do painel em produção.
    allow_credentials=False,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)


class DadosSensores(BaseModel):
    codigo_esp32: str
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
    print(f"ESP32: {dados.codigo_esp32}")
    print(f"Temperatura: {dados.temperatura} °C")
    print(f"Umidade do ar: {dados.umidade_ar} %")
    print(f"Umidade do solo: {dados.umidade_solo} %")

    with conectar_banco() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("""
                INSERT INTO public.leituras (
                    codigo_esp32,
                    temperatura,
                    umidade_ar,
                    umidade_solo
                )
                VALUES (%s, %s, %s, %s)
            """, (
                dados.codigo_esp32,
                dados.temperatura,
                dados.umidade_ar,
                dados.umidade_solo
            ))

    return {
        "status": "ok",
        "mensagem": "Dados recebidos e salvos no banco",
        "codigo_esp32": dados.codigo_esp32
    }


@app.get("/dados")
def listar_dados():
    with conectar_banco() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("""
                SELECT
                    id,
                    codigo_esp32,
                    temperatura,
                    umidade_ar,
                    umidade_solo,
                    data_hora
                FROM public.leituras
                ORDER BY data_hora DESC
            """)

            resultados = cursor.fetchall()

    dados = []

    for linha in resultados:
        dados.append({
            "id": linha[0],
            "codigo_esp32": linha[1],
            "temperatura": linha[2],
            "umidade_ar": linha[3],
            "umidade_solo": linha[4],
            "data_hora": linha[5]
        })

    return dados
