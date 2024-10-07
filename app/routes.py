from flask import Blueprint, jsonify, request
from flasgger import Swagger
from .models import Veiculos
from . import db

bp = Blueprint("veiculos", __name__)


# Rota para Listar Todos os Veículos
@bp.route("/veiculos", methods=["GET"])
def get_veiculos():
    """
    Listar todos os veículos cadastrados.
    ---
    tags:
        - Veiculos
    responses:
      200:
        description: Lista de veículos
    """
    veiculos = Veiculos.query.all()
    return jsonify([veiculo.serialize() for veiculo in veiculos])


# Rota para Listar um Veículo Específico
@bp.route("/veiculos/<int:veiculo_id>", methods=["GET"])
def get_veiculo(veiculo_id):
    """
    Rota para listar um veículo específico.
    ---
    tags:
        - Veiculos
    parameters:
      - name: veiculo_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Veículo encontrado
      404:
        description: Veículo não encontrado
    """
    veiculo = Veiculos.query.get(veiculo_id)
    if veiculo is None:
        return jsonify({"mensagem": "Veículo não encontrado"}), 404
    return jsonify(veiculo.serialize())


# Rota para Criar um Novo Veículo
@bp.route("/veiculos", methods=["POST"])
def create_veiculo():
    """
    Rota para criar um novo veículo.
    ---
    tags:
        - Veiculos
    parameters:
      - name: veiculo
        in: body
        required: true
        schema:
          type: object
          properties:
            marca:
              type: string
            modelo:
              type: string
            ano:
              type: integer
            preco:
              type: number
    responses:
      201:
        description: Veículo criado com sucesso
      400:
        description: Dados inválidos ou incompletos
    """
    dados = request.get_json()

    # Verifica se os dados são um objeto (não uma lista) e estão completos
    if not isinstance(dados, dict):
        return jsonify({"erro": "Esperado um único objeto, não uma lista."}), 400

    if (
        "marca" not in dados
        or "modelo" not in dados
        or "ano" not in dados
        or "preco" not in dados
    ):
        return jsonify({"erro": "Dados do veículo incompletos ou inválidos"}), 400

    # Cria o novo veículo
    novo_veiculo = Veiculos(
        marca=dados["marca"],
        modelo=dados["modelo"],
        ano=dados["ano"],
        preco=dados["preco"],
    )
    db.session.add(novo_veiculo)
    db.session.commit()

    return jsonify({"mensagem": "Veículo criado com sucesso!"}), 201


# Rota para Atualizar um Veículo
@bp.route("/veiculos/<int:veiculo_id>", methods=["PUT"])
def update_veiculo(veiculo_id):
    """
    Rota para atualizar um veículo.
    ---
    tags:
        - Veiculos
    parameters:
      - name: veiculo_id
        in: path
        type: integer
        required: true
      - name: veiculo
        in: body
        required: true
        schema:
          type: object
          properties:
            marca:
              type: string
            modelo:
              type: string
            ano:
              type: integer
            preco:
              type: number
    responses:
      200:
        description: Veículo atualizado com sucesso
      404:
        description: Veículo não encontrado
    """
    veiculo = Veiculos.query.get(veiculo_id)
    if veiculo is None:
        return jsonify({"mensagem": "Veículo não encontrado"}), 404

    dados = request.get_json()
    if "marca" in dados:
        veiculo.marca = dados["marca"]
    if "modelo" in dados:
        veiculo.modelo = dados["modelo"]
    if "ano" in dados:
        veiculo.ano = dados["ano"]
    if "preco" in dados:
        veiculo.preco = dados["preco"]

    db.session.commit()
    return jsonify(veiculo.serialize())


# Rota para Deletar um Veículo
@bp.route("/veiculos/<int:veiculo_id>", methods=["DELETE"])
def delete_veiculo(veiculo_id):
    """
    Rota para deletar um veículo.
    ---
    tags:
        - Veiculos
    parameters:
      - name: veiculo_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Veículo excluído com sucesso
      404:
        description: Veículo não encontrado
    """
    veiculo = Veiculos.query.get(veiculo_id)
    if veiculo is None:
        return jsonify({"mensagem": "Veículo não encontrado"}), 404

    db.session.delete(veiculo)
    db.session.commit()
    return jsonify({"mensagem": "Veículo excluído com sucesso"}), 200


if __name__ == "__main__":
    bp.run(debug=True)
