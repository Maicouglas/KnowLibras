import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()  # lê o arquivo .env e carrega as variáveis


def get_connection():
    """
    Abre e retorna uma conexão com o MySQL.
    As credenciais vêm do arquivo .env (nunca sobe pro GitHub).
    """
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT", "4000")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            ssl_ca=os.path.join(os.path.dirname(__file__), "isrgrootx1.pem"),
            ssl_verify_cert=True
        )
        return conn
    except Error as e:
        print(f"Erro ao conectar no MySQL: {e}")
        return None


def slugify(texto):
    """
    Transforma 'Banco de Dados' em 'banco-de-dados', tira acento,
    pra usar como chave/URL amigável.
    """
    import unicodedata
    texto = texto.strip().lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = texto.replace(" ", "-")
    return texto


def buscar_dados_glossario():
    """
    Consulta categoria + termo no MySQL e monta a mesma estrutura
    que o data.js estático tinha (LUSSLIBRAS_DATA), pra não precisar
    mudar script.js nem os outros HTMLs.
    """
    conn = get_connection()
    if conn is None:
        return {}

    dados = {}
    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id, nome, descricao FROM categoria")
        categorias = cursor.fetchall()

        for cat in categorias:
            cat_slug = slugify(cat["nome"])
            dados[cat_slug] = {
                "label": cat["nome"],
                "terms": {}
            }

        cursor.execute("""
            SELECT id, nome, descricao, video_sinal_url,
                   video_explicacao_url, categoria_id, fonte_sinal_nome
            FROM termo
        """)
        termos = cursor.fetchall()

        cat_por_id = {cat["id"]: slugify(cat["nome"]) for cat in categorias}

        for t in termos:
            cat_slug = cat_por_id.get(t["categoria_id"])
            if not cat_slug:
                continue
            termo_slug = slugify(t["nome"])
            dados[cat_slug]["terms"][termo_slug] = {
                "title": t["nome"],
                "description": t["descricao"],
                "video_sinal_url": t["video_sinal_url"],
                "video_explicacao_url": t["video_explicacao_url"],
                "fonte": t["fonte_sinal_nome"],
            }

    except Error as e:
        print(f"Erro ao consultar dados: {e}")
    finally:
        cursor.close()
        conn.close()

    return dados