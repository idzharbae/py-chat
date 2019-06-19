import os

class Config(object):
	SECRET_KEY = 'vnkdjnfjknfl1232#'
	MYSQL_HOST = 'localhost'
	MYSQL_USER = 'user'
	MYSQL_PASSWORD = 'secret'
	MYSQL_DB = 'pychat'

	SQLALCHEMY_DATABASE_URI =('mysql://user:secret@localhost/pychat')
	# SQLALCHEMY_TRACK_MODIFICATIONS = False
