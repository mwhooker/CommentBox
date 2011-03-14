import random
import glob
import os

from flask import Flask
from flask import render_template
app = Flask(__name__)

def get_hater_image(image_dir):
    return random.choice(glob.glob( os.path.join(image_dir, '*') ))


@app.route("/")
def hello():
    hater = get_hater_image('static/haters')
    return render_template('main.html', hater=hater)

if __name__ == "__main__":
    app.debug = True
    app.run()
