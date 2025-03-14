from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token
from .models import db, Transaction

bp = Blueprint('api', __name__, url_prefix='/api')

# Endpoint de prueba
@bp.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "¡El backend funciona!"}), 200

# Login simple (solo para desarrollo)
@bp.route('/login', methods=['POST'])
def login():
    # En producción, validar usuario/contraseña real
    access_token = create_access_token(identity='usuario_demo')
    return jsonify(access_token=access_token)

# --- CRUD Transactions ---
@bp.route('/transactions', methods=['POST'])
@jwt_required()
def create_transaction():
    data = request.get_json()
    new_transaction = Transaction(  
        amount=data['amount'],
        description=data.get('description', ''),
        category=data.get('category', 'Sin categoría'),
        account=data['account'],
        is_cleared=data.get('is_cleared', False)
    )
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify(new_transaction.to_dict()), 201

@bp.route('/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    transactions = Transaction.query.all()
    return jsonify([t.to_dict() for t in transactions]), 200

@bp.route('/transactions/<int:id>', methods=['PUT'])
@jwt_required()
def update_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    data = request.get_json()
    
    transaction.amount = data.get('amount', transaction.amount)
    transaction.description = data.get('description', transaction.description)
    transaction.category = data.get('category', transaction.category)
    transaction.account = data.get('account', transaction.account)
    transaction.is_cleared = data.get('is_cleared', transaction.is_cleared)
    
    db.session.commit()
    return jsonify(transaction.to_dict()), 200

@bp.route('/transactions/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    db.session.delete(transaction)
    db.session.commit()
    return jsonify({"message": "Transacción eliminada"}), 200