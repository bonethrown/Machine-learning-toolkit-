#!/bin/bash

 jobs(){
curl http://localhost:6800/schedule.json -d project=cosme -d spider=CBot
curl http://localhost:6800/schedule.json -d project=cosme -d spider=Infbot
curl http://localhost:6800/schedule.json -d project=cosme -d spider=Lafbot
curl http://localhost:6800/schedule.json -d project=cosme -d spider=Megabot
curl http://localhost:6800/schedule.json -d project=cosme -d spider=Sbot
curl http://localhost:6800/schedule.json -d project=cosme -d spider=Zbot
}

jobs
