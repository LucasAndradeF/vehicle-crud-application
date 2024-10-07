from . import db


class Veiculos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    marca = db.Column(db.String(40), nullable=False)
    modelo = db.Column(db.String(40), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "marca": self.marca,
            "modelo": self.modelo,
            "ano": self.ano,
            "preco": self.preco,
        }
