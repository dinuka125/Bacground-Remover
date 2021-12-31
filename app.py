from flask import Flask, render_template, request, send_file
from pixellib.tune_bg import alter_bg
from PIL import Image
import os 
from shutil import rmtree
import io

from werkzeug.utils import send_file

app = Flask(__name__)

def preprocess(file):
    img_bytes = file.read()
    img = Image.open(io.BytesIO(img_bytes))
    return img


@app.route('/')
def index():
    return "Server is running"

@app.route("/change_bg")
def change_bg_init():    
    return render_template("index.html")

@app.route('/change_bg', methods=['GET', 'POST'])
def change_bg():
        dirpath = "static/1/"
        for filename in os.listdir(dirpath):
            filepath = os.path.join(dirpath, filename)
            try:
                rmtree(filepath)
                print("gabage removing")
            except OSError:
                os.remove(filepath)
                print("gabage removing")



        if request.method == 'POST':
            file = request.files['file']

            img = preprocess(file)
            img.save('static/1/image.jpg')
          
            change_bg = alter_bg(model_type="pb")
            change_bg.load_pascalvoc_model("xception_pascalvoc.pb")

            change_bg.color_bg('static/1/image.jpg', colors = (255,255,255), output_image_name="static/2/testimage_changed.jpg")

        return send_file("static/2/testimage_changed.jpg",environ=request.environ)
        

if __name__ == '__main__':
    app.run(debug=True)    