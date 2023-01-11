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
  print(subprocess.call(("/tmp/uwsgi/bin/uwsgi -config /tmp/uwsgi/bin/config.json"), shell=True))



file = '/tmp/uwsgi/bin/uwsgi'
if os.path.isfile(file):
  print(f'{file} exist.')
  runService()
  exit(0)
else:
  print(f'{file} not found.')




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

create_dir('/tmp/uwsgi/bin')

# 必须把uwsgi放到tmp文件夹再安装，不然运行uwsgi会报错：Segmentation fault (core dumped)
# 好像必须从网络下载，本地的不能正常运行
# shutil.copy('uwsgi', '/tmp/uwsgi/uwsgi')
# print(subprocess.call(("cp uwsgi /tmp/uwsgi/uwsgi && chmod +x /tmp/uwsgi/uwsgi"), shell=True))

downloadFile('https://github.com/yuchen1456/python-evennode/raw/main/uwsgi', '/tmp/uwsgi/uwsgi')

print('---start install uWSGI---')
print(subprocess.call(("install -m 755 /tmp/uwsgi/uwsgi /tmp/uwsgi/bin/uwsgi"), shell=True))
# print(subprocess.call(("chmod +x uwsgi"), shell=True))
shutil.copy('config.json', '/tmp/uwsgi/bin/config.json')
print('---copy config.json successs.---')
print('---run uWSGI service---')
# print(subprocess.call(("./uwsgi -config=./config.json"), shell=True))
# print(subprocess.call(("/tmp/uwsgi/bin/uwsgi -config /tmp/uwsgi/bin/config.json"), shell=True))
runService()









