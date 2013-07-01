#!/bin/bash
echo cancelling job id: $1
curl http://localhost:6800/cancel.json -d project=cosme -d job=$1
