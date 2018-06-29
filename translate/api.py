import os
import uuid
import PyPDF2
import io

from flask import Flask, render_template, request
from flask_restful import Resource, Api
from flask_restful import reqparse
from .translate import run_translate
from google.cloud import vision
from google.protobuf.json_format import MessageToJson

from wand.image import Image

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


def ocr(imagepath, outputpath):
    client = vision.ImageAnnotatorClient()

    with io.open(imagepath, 'rb') as imagefile:
        content = imagefile.read()

    image = vision.types.Image(content=content)
    response = client.document_text_detection(image=image)

    with io.open(outputpath, 'w') as f:
        f.write(MessageToJson(response))


class Upload(Resource):
    def post(self):
        pdf = request.files['file']
        file_id = str(uuid.uuid4())

        dirpath = '/tmp/' + file_id
        os.makedirs(dirpath)

        pdfpath = os.path.join(dirpath, 'org.pdf')

        pdf.save(pdfpath)

        with open(pdfpath, 'rb') as f:
            pdf = PyPDF2.PdfFileReader(pdfpath)
            page_count = pdf.getNumPages()
            
            print("page_count:", page_count)

        imgpath = os.path.join(dirpath, 'images')
        os.makedirs(imgpath)

        for i in range(page_count):
            print("convert page:", i)
            name = "{}[{}]".format(pdfpath, i)
            with Image(filename=name, resolution=100) as image:
                image.format = 'jpeg'
                image.compression_quality = 75
                image.save(filename=os.path.join(imgpath, "{}.jpg".format(i)))

        jsonpath = os.path.join(dirpath, 'json')
        os.makedirs(jsonpath)
        for i in range(page_count):
            print("ocr page:", i)
            ocr(os.path.join(imgpath, "{}.jpg".format(i)),
                os.path.join(jsonpath, "{}.json".format(i)))

        return dict(file_id=file_id)


api.add_resource(Upload, '/upload')


@app.route('/test')
def test():
    return render_template("test.html")


if __name__ == '__main__':
    app.run(debug=True)
