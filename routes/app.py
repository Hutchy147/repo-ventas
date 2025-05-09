from flask import Flask, request, jsonify
from config import Config
from extensions import db
from models.sales import Sale
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/sales', methods=['POST'])
def create_sale():
    data = request.get_json()

    new_sale = Sale(
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        customer=data['customer'],
        discount=data['discount'],
        total=data['total']
    )
    db.session.add(new_sale)
    db.session.commit()

    return jsonify({'message': 'Sale created successfully'}), 201

@app.route('/sales', methods=['GET'])
def get_sales():
    sales = Sale.query.all()
    result = []
    for sale in sales:
        result.append({
            'id': sale.id,
            'date': sale.date.strftime('%Y-%m-%d'),
            'customer': sale.customer,
            'discount': sale.discount,
            'total': sale.total
        })
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
