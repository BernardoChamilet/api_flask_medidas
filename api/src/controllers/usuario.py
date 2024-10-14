from flask import jsonify, request
import src.repositories.usuario as repositories
import src.models.usuario as models
from flask_bcrypt import Bcrypt
from pydantic import ValidationError

bcrypt = Bcrypt()

# buscarUsuario busca dados não sensíveis de um usuário
def buscarUsuario(id):
    usuario, erro = repositories.buscarUsuario(id)
    if erro != None:
        return jsonify({"erro": erro}), 500
    elif usuario != None:
        return jsonify(usuario), 200
    else:
        return '', 204
    
# buscarUsuarios busca dados não sensíveis de todos usuários
def buscarUsuarios():
    usuarios, erro = repositories.buscarUsuarios()
    if erro != None:
        return jsonify({"erro": erro}), 500
    elif usuarios != None:
        return jsonify(usuarios), 200
    else:
        return '', 204

# criarUsuario cria um novo usuário
def criarUsuario():
    dados = request.get_json()
    try:
        usuario = models.Usuario(**dados)
    except ValidationError as e:
        return jsonify({"erro": e.errors()}), 400
    usuarioDict = usuario.model_dump()
    usuarioDict["senha"] = bcrypt.generate_password_hash(usuarioDict["senha"]).decode('utf-8')
    usuarioID, erro = repositories.criarUsuario(usuarioDict)
    if erro != None:
        return jsonify({"erro": erro}), 500
    return jsonify({"id": usuarioID}), 201

# atualizarUsuario atualiza campos de um usuário exceto senha
def atualizarUsuario(id):
    dados = request.get_json()
    try:
        usuario = models.Usuario(**dados)
    except ValidationError as e:
        return jsonify({"erro": e.errors()}), 400
    linhasAtualizadas, erro = repositories.atualizarUsuario(usuario.model_dump(), id)
    if erro != None:
        return jsonify({"erro": erro}), 500
    elif linhasAtualizadas == 0:
        return jsonify({"erro":"Nenhum usuário com esse id encontrado"}), 400
    else:
        return '', 204

# deletarUsuario deleta um usuario    
def deletarUsuario(id):
    linhasDeletadas, erro = repositories.deletarUsuario(id)
    if erro != None:
        return jsonify({"erro": erro}), 500
    elif linhasDeletadas == 0:
        return jsonify({"erro":"Nenhum usuário com esse id encontrado"}), 400
    else:
        return jsonify({"id":id}), 200