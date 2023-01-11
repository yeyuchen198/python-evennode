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





def create_dir(file_path):
  if os.path.exists(file_path) is False:
    os.makedirs(file_path)
    print('create_dir successs:', file_path)


def downloadFile(url, savepath):
  down_res = requests.get(url=url, params={})
  with open(savepath, "wb") as file:
    file.write(down_res.content)
  print('download success, file save at:', savepath)


def unzipFile(file, savepath):
  print('unzipFile...')
  zip_file = zipfile.ZipFile(file)
  for f in zip_file.namelist():
    zip_file.extract(f, savepath)
    print(f)
  zip_file.close()
  print(f'unzip {file} success.')


def runService():
  shutil.copy('config.json', '/tmp/xray/bin/config.json')
  print('---run xray service---')
  print(
    subprocess.call(("/tmp/xray/bin/xray -config  /tmp/xray/bin/config.json"),
                    shell=True))


file = '/tmp/xray/bin/xray'
if os.path.isfile(file):
  print(f'{file} exist.')
  runService()
  exit(0)
else:
  print(f'{file} not found.')

create_dir('/tmp/xray/bin')

url = 'https://github.com/XTLS/Xray-core/releases/latest/download/Xray-linux-64.zip'
savepath = '/tmp/xray/xray.zip'
downloadFile(url, savepath)

# unzip /tmp/xray/xray.zip -d /tmp/xray
# install -m 755 /tmp/xray/xray /tmp/xray/bin/xray

unzipFile(savepath, '/tmp/xray')
print('---start install xray---')
print(
  subprocess.call(("install -m 755 /tmp/xray/xray /tmp/xray/bin/xray"),
                  shell=True))

shutil.copy('config.json', '/tmp/xray/bin/config.json')
print('---copy config.json successs.---')
runService()
