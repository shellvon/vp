from flask import Flask
from api import api

def create_app(config_file):
    app = Flask(__name__)
    app.config.from_object(config_file)
    return app


app = create_app('setting')

app.register_blueprint(api)

def main():
    app.run(host=app.config.get('HOST'))

if __name__ == '__main__':
    main()

