#!/bin/bash
curl -i -H "Content-Type: application/json" -X POST -d @testconfig.json http://127.0.0.1:5000/config
#curl -i -H "Content-Type: application/json" -X POST -d @testfile_remFCA.json http://127.0.0.1:5353/remove
#curl -i -H "Content-Type: application/json" -X POST  http://127.0.0.1:5353/clear

