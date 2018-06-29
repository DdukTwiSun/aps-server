import os
import uuid
import PyPDF2
import io

from multiprocessing import Pool

from flask import Flask, render_template, request, url_for, send_file
from flask_restful import Resource, Api
from flask_restful import reqparse
from flask_cors import CORS
from .translate import run_translate
from google.cloud import vision

from wand.image import Image

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.abspath('./uploads')
CORS(app)
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

            translated_text = run_translate(_text, _source, _target)

            return {'Text': args['text'],
                    'Source': args['source'],
                    'Target': args['target'],
                    'TranslatedText': translated_text,
                    }
        except Exception as e:
            return {'error': str(e)}


api.add_resource(Translate, '/translate')


def ocr(imagepath):
    client = vision.ImageAnnotatorClient()

    with io.open(imagepath, 'rb') as imagefile:
        content = imagefile.read()

    image = vision.types.Image(content=content)
    response = client.document_text_detection(image=image)

    return response


def unmarshal_gcv_box(bounding_box):
    vertices = bounding_box.vertices
    x_list = list(map(lambda i: i.x, vertices))
    y_list = list(map(lambda i: i.y, vertices))
    min_x = min(x_list)
    max_x = max(x_list)
    min_y = min(y_list)
    max_y = max(y_list)

    width = max_x - min_x
    height = max_y - min_y

    return dict(x=min_x, y=min_y, width=width, height=height)


def symbols_to_text(symbols):
    return "".join(map(lambda x: x.text, symbols))


def arrange_paragraph(par):
    bounding_box = unmarshal_gcv_box(par.bounding_box)
    text = " ".join(map(lambda x: symbols_to_text(x.symbols), par.words))

    return dict(
            bounding_box=bounding_box,
            text=text)


def convert_gcv_ocr_to_json(gvr_response):
    annotation = gvr_response.full_text_annotation
    pages = annotation.pages

    assert(len(pages) == 1)

    paragraphs = []

    for page in pages:
        for block in page.blocks:
            for par in block.paragraphs:
                paragraphs.append(arrange_paragraph(par))

    return paragraphs


def process_ocr(args):
    file_id, page, pdfpath = args
    dirpath = os.path.join(app.config['UPLOAD_FOLDER'], file_id)
    imgdir = os.path.join(dirpath, 'images')
    imgpath = os.path.join(imgdir, "{}.jpg".format(page))
    convert_to_img(pdfpath, page, imgpath)

    ocr = ocr_image(imgpath)
    return ocr

def convert_to_img(pdfpath, page, imgpath):
    pdfname = "{}[{}]".format(pdfpath, page)
    print("convert page:", pdfname, imgpath)
    with Image(filename=pdfname, resolution=100) as image:
        image.format = 'jpeg'
        image.compression_quality = 75
        image.save(filename=imgpath)

def ocr_image(imgpath):
    response = ocr(imgpath)
    ocrdata = convert_gcv_ocr_to_json(response)
    return ocrdata

pool = Pool(processes=4)


class Upload(Resource):
    def post(self):
        pdf = request.files['file']
        file_id = str(uuid.uuid4())

        dirpath = os.path.join(app.config['UPLOAD_FOLDER'], file_id)
        os.makedirs(dirpath)

        pdfpath = os.path.join(dirpath, 'org.pdf')

        pdf.save(pdfpath)

        pdf = PyPDF2.PdfFileReader(pdfpath)
        page_count = pdf.getNumPages()

        print("page_count:", page_count)

        imgdir = os.path.join(dirpath, 'images')
        os.makedirs(imgdir)

        args = map(lambda i: (file_id, i, pdfpath), range(page_count))
        ocrs = pool.map(process_ocr, args)

        pages = []
        for idx, ocr in enumerate(ocrs):
            page = {}
            page['ocr'] = ocr
            page['image'] = url_for(
                'doc',
                file_id=file_id,
                filename='{}.jpg'.format(idx),
                _external=True)
            pages.append(page)

        return dict(file_id=file_id, pages=pages)


api.add_resource(Upload, '/upload')


@app.route('/test')
def test():
    return render_template("test.html")


@app.route('/images/<file_id>/<filename>')
def doc(file_id, filename):
    path = os.path.join(
            app.config['UPLOAD_FOLDER'], file_id, 'images', filename)
    return send_file(path)


if __name__ == '__main__':
    app.run(debug=True)
