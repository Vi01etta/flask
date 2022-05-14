import flask
import os
from flask import request, jsonify
from flask.views import MethodView
from sqlalchemy import Column, DateTime, Integer, create_engine, String, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = flask.Flask('app')
PG_DSN = os.getenv('PG_DSN')
engine = create_engine(PG_DSN)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class AdModel(Base):
    __tablename__ = 'ads'
    id = Column(Integer, primary_key=True)
    header = Column(String(200), nullable=False)
    description = Column(String(500), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    owner = Column(String(200), nullable=False)

    def __repr__(self):
        return f'AdModel: {self.header}'

    def to_dict(self):
        return {
            'id': self.id,
            'header': self.header,
            'description': self.description,
            'created_at': self.created_at,
            'owner': self.owner,

        }


Base.metadata.create_all(engine)


class HttpError(Exception):

    def __init__(self, error_code, message):
        self.error_code = error_code
        self.message = message


@app.errorhandler(HttpError)
def handle_error(error):
    response = jsonify({
        'message': error.message
    })
    response.status_code = error.status_code
    return response


class AdView(MethodView):

    def get(self):
        with Session() as session:
            ads = session.query(AdModel).all()
            return jsonify([ad.to_dict() for ad in ads])

    def get_ad(self, ad_id):
        with Session() as session:
            ads = session.query(AdModel).filter_by(id=ad_id).one()
        return jsonify(ads.to_dict())

    def post(self):
        new_ad_data = request.json
        with Session() as session:
            new_ad = AdModel(**new_ad_data)
            session.add(new_ad)
            session.commit()
            return jsonify({
                'id': new_ad.id,
                'header': new_ad.header,
                    })
    #
    def delete(self, ad_id):
        with Session() as session:
            ads = session.query(AdModel).filter_by(id=ad_id).one()
            session.delete(ads)
            session.commit()
        return {'204': 'no content'}

app.add_url_rule('/ad/', view_func=AdView.as_view('create_ad'), methods=['POST'])
app.add_url_rule('/ad/', view_func=AdView.as_view('get_all'), methods=['GET'])
app.add_url_rule('/ad/<int:ad_id>', view_func=AdView.as_view('get_ad'), methods=['GET', 'DELETE'])
