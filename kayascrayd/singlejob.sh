#!/bin/bash
scrapy deploy  -p  cosme
echo scheduling single spider: $1
curl http://localhost:7000/schedule.json -d project=cosme -d spider=$1
