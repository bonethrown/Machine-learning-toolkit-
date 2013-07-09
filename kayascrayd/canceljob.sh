#!/bin/bash
echo cancelling job id: $1
curl http://localhost:7000/cancel.json -d project=cosme -d job=$1
