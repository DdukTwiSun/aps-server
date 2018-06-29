from flask import Flask, render_template
from flask_restful import Resource, Api
from flask_restful import reqparse
from .translate import run_translate

app = Flask(__name__)
api = Api(app)


class Translate(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('text', type=str)
            parser.add_argument('source', type=str)
            parser.add_argument('target', type=str)
            args = parser.parse_args()

            _text = args['text']
            _source = args['source']
            _target = args['target']

            translated_text = run_translate(_text,_source,_target)

            return {'Text': args['text'],
                    'Source': args['source'],
                    'Target': args['target'],
                    'TranslatedText': translated_text,
                    }
        except Exception as e:
            return {'error': str(e)}


api.add_resource(Translate, '/translate')


@app.route('/test')
def test():
    return render_template("test.html")


if __name__ == '__main__':
    app.run(debug=True)
