import time
from models import Transactions
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from decimal import Decimal
import pymysql
pymysql.install_as_MySQLdb()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:MyNewPass@localhost/credit_card_transactions'
db = SQLAlchemy(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/<user_id>/transactions')
def transactions(user_id):
    resp = Transactions.query.filter(Transactions.user_id == user_id).all()
    return jsonify({
        'data': [transaction.serialize for transaction in resp]
    })

@app.route('/<user_id>/onehour_transactions')
def onehour_transactions(user_id):
    end_time = time.time()
    start_time = end_time - 60 * 60  # 1 hour
    resp = Transactions.query.filter(Transactions.user_id == user_id, Transactions.transaction_time.between(start_time, end_time)).all()
    return jsonify({
        'data': [transaction.serialize for transaction in resp]
    })

@app.route('/<user_id>/sum')
def sum_transactions(user_id):
    resp = Transactions.query.filter(Transactions.user_id == user_id).all()
    transactions = [transaction.serialize for transaction in resp]
    result = sum([Decimal(transaction.get('transaction_amount'))
                  for transaction in transactions])
    return jsonify({
        'data': str(result)
    })


if __name__ == '__main__':
    app.run()
