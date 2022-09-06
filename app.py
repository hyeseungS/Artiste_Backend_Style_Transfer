import os
from flask import Flask, request
from flask.templating import render_template
from werkzeug.utils import secure_filename
from style_transfer import main

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/nst_get')
def nst_get():
    return render_template('nst_get.html')


@app.route('/nst_post', methods=['GET', 'POST'])
def transfer():
    if request.method == 'POST':
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
        transfer_img_path = './static/images/' + str(transfer_img.split('/')[-1])

        return render_template('nst_post.html',
                               style_img=style_img_path, content_img=content_img_path, transfer_img=transfer_img_path)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)
