# coding: utf-8
from flask_jwt_extended import get_jwt_identity, decode_token

from app.extensions import db
from sqlalchemy import or_, and_


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    username = db.Column(db.String)
    password = db.Column(db.String)
    status = db.Column(db.String)
    role = db.Column(db.String)
    create_date = db.Column(db.Integer)

    def convert_json(self):
        return dict(
            id=self.id,
            username=self.username,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
            status=self.status,
            role=self.role,
            create_date=self.create_date
        )

    @staticmethod
    def get_all():
        return User.query.order_by(User.username).all()

    @staticmethod
    def get_total_number():
        return User.query.count()

    @staticmethod
    def get_current_user():
        return User.query.get(get_jwt_identity())

    @staticmethod
    def get_by_id(_id):
        return User.query.get(_id)

    @classmethod
    def find_by_user_filter(cls, filter_name=None, role=None, status=None):
        """
        :param filter_name:
        :param role:
        :param status:
        :return: return json array
        """
        results = []
        if filter_name is None:
            datas = cls.query.all()
        else:
            datas = cls.query.filter(
                or_(cls.username.like('%{}%'.format(filter_name), escape='\\'),
                    cls.first_name.like('%{}%'.format(filter_name), escape='\\'),
                    cls.last_name.like('%{}%'.format(filter_name), escape='\\')))

        for user in datas:
            results.append(user.convert_json())
        if status:
            results = list(filter(lambda s: s['status'] == status, results))
        if role:
            results = list(filter(lambda s: s['role'] == role, results))
        return results

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class Token(db.Model):
    __tablename__ = 'token'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jti = db.Column(db.String(255))
    token_type = db.Column(db.String)
    user_identity = db.Column(db.String)
    revoked = db.Column(db.Boolean)
    expires = db.Column(db.Integer)

    def __init__(self, jti=None, token_type=None, user_identity=None, revoked=None, expires=None):
        self.id = None
        self.jti = jti
        self.token_type = token_type
        self.user_identity = user_identity
        self.revoked = revoked
        self.expires = expires

    def json(self):
        return dict(
            id=self.id,
            jti=self.jti,
            token_type=self.token_type,
            user_identity=self.user_identity,
            revoked=self.revoked,
            expires=self.expires
        )

    @classmethod
    def parse_to_object(self, encoded_token=None):
        data = Token()
        decoded_token = decode_token(encoded_token)
        data.jti = decoded_token['jti']
        data.user_identity = decoded_token['identity']
        data.token_type = decoded_token['type']
        data.expires = decoded_token['exp']
        data.revoked = 0
        return data

    @classmethod
    def save_to_db(self, encoded_token=None):
        try:
            token = self.parse_to_object(encoded_token=encoded_token)
            db.session.add(token)
            db.session.commit()
        except Exception as e:
            print(e.__str__())

    @classmethod
    def revoke_token(self, jti):
        """
        Revokes the given token. Raises a TokenNotFound error if the token does
        not exist in the database
        """
        try:
            token = Token.query.filter_by(jti=jti).first()
            token.revoked = True
            db.session.commit()
        except Exception as e:
            print(e.__str__())

    @staticmethod
    def is_token_revoked(decoded_token):
        """
        Checks if the given token is revoked or not. Because we are adding all the
        tokens that we create into this database, if the token is not present
        in the database we are going to consider it revoked, as we don't know where
        it was created.
        """
        jti = decoded_token['jti']
        try:
            token = Token.query.filter_by(jti=jti).one()
            return token.revoked
        except Exception:
            return True


class Data(db.Model):
    __tablename__ = 'data'

    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    published = db.Column(db.String)

    def convert_json(self):
        return dict(
            id=self.id,
            title=self.title,
            description=self.description,
            published=self.published
        )

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()
