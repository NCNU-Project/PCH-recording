import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI ='mysql+pymysql://' + ( os.environ.get("DATABASE_URI") or 'kamailio:kamailiorw@127.0.0.1/kamailio')
    FILE_ROOT_DIRECTORY=os.environ.get("FILE_ROOT_DIRECTORY") or "./"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
