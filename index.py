#!/usr/bin/python
from flask import Flask, jsonify, abort, make_response, request
import subprocess

app = Flask(__name__)

@app.route('/')
def saludo():
	return jsonify({"response":"Web VBoxManage Service"})

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
       
@app.route('/machines/changeName', methods=['POST'])
def changeNameMac():
       if not request.json or not 'newname' or not 'osname' in request.json:
              abort(400)
       osName = request.json['osname']
       newName = request.json['newname']
       p1 = subprocess.run(["VBoxManage", "modifyvm", osName, "--name", newName], stdout=subprocess.PIPE)
       out = p1.stdout.decode('ascii')
       return jsonify({'response': 'name updated'})

@app.route('/machines/changeCpus', methods=['POST'])
def changeCpus():
       if not request.json or not 'cpus' or not 'osname' in request.json:
              abort(400)
       osName = request.json['osname']
       cpusNumber = request.json['cpus']
       p1 = subprocess.run(["VBoxManage", "modifyvm", osName, "--cpus", cpusNumber], stdout=subprocess.PIPE)
       out = p1.stdout.decode('ascii')
       return jsonify({'response': 'cps updated'})

@app.route('/machines/changeMemory', methods=['POST'])
def changeMemory():
       if not request.json or not 'memory' or not 'osname' in request.json:
              abort(400)
       osName = request.json['osname']
       memoryNumber = request.json['memory']
       p1 = subprocess.run(["VBoxManage", "modifyvm", osName, "--memory", memoryNumber], stdout=subprocess.PIPE)
       out = p1.stdout.decode('ascii')
       return jsonify({'response': 'memory updated'})



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

