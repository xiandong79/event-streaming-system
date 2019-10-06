from exts import db


class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String())
    transaction_amount = db.Column(db.String())
    transaction_time = db.Column(db.DECIMAL())

    @property
    def serialize(self):
        """Return object data in serializeable format"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'transaction_amount': self.transaction_amount,
            'transaction_time': self.transaction_time,
        }
