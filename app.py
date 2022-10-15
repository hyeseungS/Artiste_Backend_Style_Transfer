import base64
import io
import os

from PIL import Image
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
from style_transfer import main

app = Flask(__name__)


@app.route('/transfer', methods=['POST'])
def transfer():
    # Style Image
    style_img = request.files['style_img']
    style_img.save('./static/images/' + str(style_img.filename))
    style_img_path = './static/images/' + str(style_img.filename)

    # Content Image
    content_img = request.files['content_img']
    content_img.save('./static/images/' + str(content_img.filename))
    content_img_path = './static/images/' + str(content_img.filename)

    # Style Transfer
    transfer_img = main(style_img_path, content_img_path)
    transfer_img_path = os.getcwd() + '/static/images/' + str(transfer_img.split('/')[-1])

    # base64 image
    binary_image = convertToBinaryData(transfer_img_path)
    binary_str = binary_image.decode('utf-8')

    return jsonify({"transfer": binary_str})

@app.route('/sample', methods=['POST'])
def sample():
    # Sample Image
    sample_img = request.files['sample_img']
    sample_img.save('./static/images/' + str(sample_img.filename))
    sample_img_path = os.getcwd() + '/static/images/' + str(sample_img.filename)
    binary_image = convertToBinaryData(str(sample_img_path))

    binary_str = binary_image.decode('utf-8')

    # string to bytes
    img_new_bytes = binary_str.encode(encoding="utf-8")
    img_new_bytes = base64.b64decode(img_new_bytes)

    # 이미지 출력
    image = Image.open(io.BytesIO(img_new_bytes))
    image.show()

    return jsonify({"sample": binary_str})

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = base64.b64encode(file.read())
    return binaryData


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)
