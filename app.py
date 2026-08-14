import json
from flask import Flask, render_template, request, Response
from db import buscar_dados_glossario

app = Flask(__name__)


@app.route('/')
def index():
    query = request.args.get('q', '')
    return render_template('index.html', query=query)


@app.route('/categoria')
def categoria():
    return render_template('categoria.html')


@app.route('/termo')
def termo():
    return render_template('termo.html')


@app.route('/static/js/data.js')
def data_js():
    """
    Gera o data.js dinamicamente a partir do MySQL, no lugar do
    arquivo estático antigo. O front-end (script.js, index.html,
    categoria.html, termo.html) continua igual, pois o resultado
    final ainda é: const KNOWLIBRAS_DATA = {...};
    """
    dados = buscar_dados_glossario()
    conteudo = f"const KNOWLIBRAS_DATA = {json.dumps(dados, ensure_ascii=False)};"
    return Response(conteudo, mimetype='application/javascript')


if __name__ == '__main__':
    app.run(debug=True)