#!/bin/python
###############################################
###Selfnet YouQoS sensor module####
#####M.Ulbricht 2017 ulbricht@innoroute.de#####
###############################################

# use only for testing code is prone to injection attacks!

from flask import Flask
from flask import request
from flask import jsonify
import requests
import sqlite3
import json
import os
#import logging
#log = logging.getLogger('werkzeug')
#log.setLevel(logging.ERROR)
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

max_priority=3
dbname='youqos.db'
push_url='http://192.168.61.1:5001'
user_maxflows=1
conn = sqlite3.connect(dbname)
c = conn.cursor()
c.execute('DELETE FROM user_flows;')#clear tables
conn.commit()

print('starting REST...')

def run(command):
		command=command + ">lastlog"
		if os.system(command) == 0:
			with open('lastlog', 'r') as lastlog:
				return jsonify({'status': 'ok', 'log': lastlog.read()}), 201
		else:
			with open('lastlog', 'r') as lastlog:
				return jsonify({'status': 'error', 'log': lastlog.read()}), 400


@app.route('/config', methods=['POST'])
def setcfg():
		global max_priority
		global dbname
		global push_url
		global user_maxflows
		r = request.json
		if not r or not 'push_url' in r or not 'user_maxflows' in r:
			return jsonify({'status': 'error'}), 406
		push_url=r.get('push_url')
		user_maxflows=r.get('user_maxflows')    
		return jsonify({'status': 'ok', 'log': 'config set successfull'}), 201

@app.route('/addflow', methods=['POST'])
def addflow():
		global max_priority
		global dbname
		global push_url
		global user_maxflows
		r = request.json
		if not r or not 'ip_usr' in r or not 'ip_dst' in r or not 'port_usr' in r or not 'port_dst' in r or not 'priority' in r:
			return jsonify({'status': 'error', 'log': 'parameters missing'}), 406
		conn = sqlite3.connect(dbname)
		c = conn.cursor()
		qdata=(r.get('ip_usr'),r.get('ip_dst'),r.get('port_usr'),r.get('port_dst'),)
		c.execute('SELECT COUNT(*) FROM user_flows WHERE ip_usr=? and ip_dst=? and port_usr=? and port_dst=?',qdata)
		count=c.fetchone()[0]
		if count >= 1 :
			return jsonify({'status': 'error', 'log':'flow already exists' }), 406
		qdata=(r.get('ip_usr'),)
		c.execute('SELECT COUNT(*) FROM user_flows WHERE ip_usr=?',qdata)
		count=c.fetchone()[0]
		if count >= user_maxflows :
			return jsonify({'status': 'error', 'log':'user-flow-limit reached' }), 406
		qdata=(r.get('ip_usr'),r.get('ip_dst'),r.get('port_usr'),r.get('port_dst'),r.get('priority'),1,)
		c.execute('INSERT INTO user_flows ("ip_usr","ip_dst","port_usr","port_dst","priority","type") VALUES (?,?,?,?,?,?)',qdata)
		conn.commit()
		command='curl -s -o lastlog -i -H "Content-Type: application/json" -X POST -d'
		command=command + ' \'{"ip_usr":"%s","ip_dst":"%s","port_usr":%s,"port_dst":%s,"priority":%i}\' '%(r.get('ip_usr'),r.get('ip_dst'),r.get('port_usr'),r.get('port_dst'),r.get('priority'))
		command=command + push_url + '/addYouQoSflow'
		return run(command)

@app.route('/delflow', methods=['POST'])
def delflow():
		global max_priority
		global dbname
		global push_url
		global user_maxflows
		r = request.json
		if not r or not 'ip_usr' in r or not 'ip_dst' in r or not 'port_usr' in r or not 'port_dst' in r:
			return jsonify({'status': 'error', 'log': 'parameters missing'}), 406
		conn = sqlite3.connect(dbname)
		c = conn.cursor()
		qdata=(r.get('ip_usr'),r.get('ip_dst'),r.get('port_usr'),r.get('port_dst'),)
		c.execute('DELETE FROM user_flows WHERE ip_usr=? and ip_dst=? and port_usr=? and port_dst=?',qdata)
		conn.commit()
		command='curl -s -o lastlog -i -H "Content-Type: application/json" -X POST -d'
		command=command + ' \'{"ip_usr":"%s","ip_dst":"%s","port_usr":%s,"port_dst":%s}\' '%(r.get('ip_usr'),r.get('ip_dst'),r.get('port_usr'),r.get('port_dst'))
		command=command + push_url + '/delYouQoSflow'
#		return jsonify({'status': 'ok', 'log': 'done'}), 200
		return run(command)




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


