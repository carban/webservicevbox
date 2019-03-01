#!/usr/bin/python
from flask import Flask, jsonify, abort, make_response, request
import subprocess

app = Flask(__name__)


@app.route('/')
def saludo():
	return jsonify({"response":"Web VBoxManage Service"})
#Example
#curl -i http://localhost:5000

def splitnames(l):
       arr = []
       for i in range(0, len(l), 2):
              arr.append(l[i])
       return arr

@app.route('/machines/list')
def ls():
       p1 = subprocess.run(["VBoxManage", "list", "vms"], stdout = subprocess.PIPE)
       out = p1.stdout.decode('ascii')
       res = splitnames(out.split())
       return jsonify({'response':res})
    
#Example
#curl -i http://localhost:5000/machines/list


@app.route('/machines/info/<string:macName>', methods=['GET'])
def infoMac(macName):
       p1 = subprocess.run(["VBoxManage", "showvminfo", macName], stdout=subprocess.PIPE)
       out = p1.stdout.decode('ascii')
       spliter = out.split()
       ajson = {
       "Name": spliter[1],
       "Groups": spliter[3],
       "Guest OS": [spliter[6], spliter[7]],
       "Config File": [spliter[12], spliter[13]],
       "Snapshot Folder": [spliter[16], spliter[17]],
       "Log Folder": [spliter[20], spliter[21]],
       "Memory Size": spliter[27],
       "VRAM size": spliter[33],
       "Number of CPUs": spliter[47]
       }
       return jsonify({'info':ajson}) 

#Example
#curl -i http://localhost:5000/info/first


@app.route('/machines/changeName', methods=['POST'])
def changeNameMac():
       if not request.json or not 'newname' or not 'osname' in request.json:
              abort(400)
       osName = request.json['osname']
       newName = request.json['newname']
       p1 = subprocess.run(["VBoxManage", "modifyvm", osName, "--name", newName], stdout=subprocess.PIPE)
       out = p1.stdout.decode('ascii')
       return jsonify({'response': 'name updated'})

#Example
#curl -H "Content-Type: application/json" -X POST -d '{"osname": "first", "newname": "primero"}' http://localhost:5000/machines/changeName


@app.route('/machines/changeCpus', methods=['POST'])
def changeCpus():
       if not request.json or not 'cpus' or not 'osname' in request.json:
              abort(400)
       osName = request.json['osname']
       cpusNumber = request.json['cpus']
       p1 = subprocess.run(["VBoxManage", "modifyvm", osName, "--cpus", cpusNumber], stdout=subprocess.PIPE)
       out = p1.stdout.decode('ascii')
       return jsonify({'response': 'cps updated'})
    
#Example
#curl -H "Content-Type: application/json" -X POST -d '{"osname": "first", "cpus": "4"}' http://localhost:5000/machines/changeCpus




@app.route('/machines/changeMemory', methods=['POST'])
def changeMemory():
       if not request.json or not 'memory' or not 'osname' in request.json:
              abort(400)
       osName = request.json['osname']
       memoryNumber = request.json['memory']
       p1 = subprocess.run(["VBoxManage", "modifyvm", osName, "--memory", memoryNumber], stdout=subprocess.PIPE)
       out = p1.stdout.decode('ascii')
       return jsonify({'response': 'memory updated'})

#Example
#curl -H "Content-Type: application/json" -X POST -d '{"osname": "first", "memory": "1024"}' http://localhost:5000/machines/changeMemory


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

