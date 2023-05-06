import typst
import tempfile
import pathlib
import os
import logging
from flask import Flask, request, jsonify, make_response

app = Flask("typst-http-api")

# set logging level
gunicorn_logger = logging.getLogger("gunicorn.error")
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)


@app.route("/", methods=["POST"])
def build():
    typst_bytes = request.get_data()
    temporary_file = tempfile.NamedTemporaryFile(
        mode="w+b", suffix=".typ", prefix=os.path.basename(__file__)
    )
    with open(temporary_file.name, mode="w+b") as f:
        f.write(typst_bytes)
    try:
        pdf_bytes = typst.compile(pathlib.Path(temporary_file.name))
    except RuntimeError as e:
        error_stringified = str(e).replace("\n", " ")
        resp = make_response(jsonify({"error": error_stringified}), 422)
        resp.headers["Content-Type"] = "application/json"
        app.logger.info(
            f"Failed to build {len(typst_bytes)} typst markup bytes: {error_stringified} "
        )
        return resp

    app.logger.info(
        f"Successfully built {len(pdf_bytes)} pdf bytes from {len(typst_bytes)} typst markup bytes"
    )
    return pdf_bytes, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
