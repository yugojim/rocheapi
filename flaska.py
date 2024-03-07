from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import http.client
import json
import ssl
url="fhir-stage-jp.tumorboard.navify.com"
port = 443

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

###serverstatus###
@app.route('/', methods=['GET'])
@cross_origin()
def serverstatus():
    return jsonify({'Server Status' : 'run'}), 200

###DischargeSummary###

@app.route('/RocheCancerBundle/', methods=['POST'])
@cross_origin()
def create_DischargeSummary():
    payload = request.data
    headers = {
      'Content-Type': 'application/json'
    }
    # SSL 金鑰和憑證文件的路徑
    cert_path = 'client.crt'
    key_path = 'client.key'
    #ca_path = 'ca.crt'
    # 金鑰的密碼
    password = b'roche_vgh'

    # 创建 SSL 上下文
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context.load_cert_chain(certfile=cert_path, keyfile=key_path, password=password)
    conn = http.client.HTTPSConnection(url, port, context=context)
    conn.request("POST", "/api/hl7-fhir-message/validate/fhirmessage", payload, headers)
    response = conn.getresponse()
    #print(response.status, response.reason)
    res=response.read().decode()
    return json.loads(res), response.status
    #return jsonify(response.read().decode()), 200

if __name__ == '__main__':
    #app.run(host="0.0.0.0", port=8100, debug=False)
	app.run(port=8100, debug=True)

