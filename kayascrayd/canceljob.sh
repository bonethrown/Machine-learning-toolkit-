#!/bin/bash
echo cancelling job id: $1
curl http://localhost:7000/cancel.json -d project=cosme -d job=$1
curl http://localhost:7000/cancel.json -d project=cosme -d job=$2
curl http://localhost:7000/cancel.json -d project=cosme -d job=$1
curl http://localhost:7000/cancel.json -d project=cosme -d job=$2
curl http://localhost:7000/cancel.json -d project=cosme -d job=$3
curl http://localhost:7000/cancel.json -d project=cosme -d job=$1
curl http://localhost:7000/cancel.json -d project=cosme -d job=$2
curl http://localhost:7000/cancel.json -d project=cosme -d job=$3
curl http://localhost:7000/cancel.json -d project=cosme -d job=$3
