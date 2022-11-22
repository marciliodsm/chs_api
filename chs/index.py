from flask import Flask, jsonify
from flask_cors import cross_origin
from chs.indicadores.compras_anteriores import ComprasAnteriores

app = Flask(__name__)


@cross_origin()
@app.route("/")
def hello_world():
    return "E aí Mundo!"

#endpoint para o indicador por mês e ano
@app.route("/indicador_compras_anteriores/<int:mes>/<int:ano>")
@cross_origin()
def get_compras_anteriores(mes, ano):
    indicadores = ComprasAnteriores().get_indicador_meses_anteriores(mes, ano)
    return jsonify(indicadores)

#endpoint para o indicador por mês e ano
@app.route("/resumo_indicador_compras_anteriores/<int:mes>/<int:ano>")
@cross_origin()
def get_resumo_compras_anteriores(mes, ano):
    indicadores = ComprasAnteriores().get_indicador_resumo(mes, ano)
    return jsonify(indicadores)