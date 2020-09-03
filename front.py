import os
from flask import Flask, jsonify, make_response, request, abort, render_template

app = Flask(__name__)

log = app.logger


@app.errorhandler(412)
def version_mismatch(error):
    return 'Version mismatch. Expected: {}: {}.{}'.format(
        X_BROKER_API_VERSION_NAME,
        X_BROKER_API_MAJOR_VERSION,
        X_BROKER_API_MINOR_VERSION), 412



@app.route('/')
def index():
    return render_template("index.html")


# @app.route('/ping')
# def ping():
#     process = subprocess.Popen(['ping', '-c 2', 'TLSPBAOSAD02'], stdout=subprocess.PIPE, universal_newlines=True)
#     while True:
#         output = process.stdout.readline()
#         print(output.strip())
#         return_code = process.poll()
#         if return_code is not None:
#             print('RETURN CODE', return_code)
#             for output in process.stdout.readlines():
#                 return jsonify(output.strip())
#             break
#         else:
#             print('RETURN CODE = None')



if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=int(os.getenv('VCAP_APP_PORT', '9094')))