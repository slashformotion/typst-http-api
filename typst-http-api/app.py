import typst 
import tempfile
import pathlib
import os
from flask import Flask, request
app = Flask("typst-http-api")



@app.route('/', methods= ["POST"])
def hello_world():
    tfile = tempfile.NamedTemporaryFile(mode="w+b", suffix='.typ', prefix=os.path.basename(__file__))
    with open(tfile.name, mode="w+b") as f:
        f.write(request.data)
    pdf_bytes = typst.compile(pathlib.Path(tfile.name))
    return pdf_bytes

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)