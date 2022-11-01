from Modules.routes import app
import os

service_port = os.environ['SERVICE_PORT']

app.run(host='0.0.0.0',port=service_port,debug=True)