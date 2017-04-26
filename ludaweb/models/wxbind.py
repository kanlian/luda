from ludaweb.models.models import db


class Wxbind(db.Model):
    __tablename__ = 'wxbinds'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    openid = db.Column(db.String(255))
    qysh = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<wxbinds %r>' % self.__tablename__

    def to_json(self):
        return {
            'id': self.id,
            'openid': self.openid,
            'qysh':  self.qysh
        }
