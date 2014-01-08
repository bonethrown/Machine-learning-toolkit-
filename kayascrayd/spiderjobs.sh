#!/bin/bash
 jobs(){
curl http://localhost:6800/schedule.json -d project=cosme -d spider=CBot
sleep 3
curl http://localhost:6800/schedule.json -d project=cosme -d spider=Infbot
sleep 3
curl http://localhost:6800/schedule.json -d project=cosme -d spider=Lafbot
sleep 3
curl http://localhost:6800/schedule.json -d project=cosme -d spider=Megabot
sleep 3
curl http://localhost:6800/schedule.json -d project=cosme -d spider=Sbot
sleep 3
curl http://localhost:6800/schedule.json -d project=cosme -d spider=Zbot
}

jobs
echo jobs
