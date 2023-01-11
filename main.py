# from flask import Flask

# app = Flask('app')

# @app.route('/')
# def hello_world():
#   return 'Hello, World!'

# app.run(host='0.0.0.0', port=8080)

# os.getenv('PORT')



import requests
import subprocess
import os
import zipfile, shutil

# print('hello world')
# print(subprocess.call(("ls -l"), shell=True))




config = '''{
  "log": {
    "loglevel": "none"
  },
  "inbounds": [
    {
      "port": PORT,
      "protocol": "VLESS",
      "settings": {
        "clients": [
          {
            "id": "3216cc34-b514-47c6-b82a-ccd37601a532"
          }
        ],
        "decryption": "none"
      },
      "streamSettings": {
        "network": "ws",
        "wsSettings": {
          "path": ""
        }
      }
    }
  ],
  "outbounds": [
    {
      "protocol": "freedom"
    }
  ]
}'''

config = config.replace('PORT', os.getenv('PORT'))
print(config)
f = open('config.json', 'w')
f.write(config)
f.close()
print('write config success')

print('---start install uWSGI---')
print(subprocess.call(("chmod +x uwsgi"), shell=True))
print('---run uWSGI service---')
print(subprocess.call(("./uwsgi -config=./config.json"), shell=True))
  

