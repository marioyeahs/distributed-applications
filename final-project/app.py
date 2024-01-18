import os
from flask import Flask, Response, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import asyncio
from json import dumps
import websockets
from websockets.exceptions import ConnectionClosedOK

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
headers ={'Access-Control-Allow-Origin': '*'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.add_url_rule(
    "/uploads/<name>", endpoint="download_file", build_only=True
)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Selecciona el archivo</title>
    <h1>Carga un nuevo archivo</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Cargar>
    </form>
    '''

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route('/client')
async def client():
    uri = "ws://localhost:5555"
    async with websockets.connect(uri) as websocket:
        with open("./uploads/video.mp4", 'rb') as file:
            data = file.read()
            await websocket.send(data)
        return Response(response=dumps({'response':"Video descargado correctamente"}), headers=headers, status = 200)






if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    
