#!/bin/bash
tgpath=/home/pi/tg
cd ${tgpath}
(sleep 3; echo "add_contact <NUMBER> <FIRSTNAME> <SECONDNAME>"; echo "msg <FIRSTNAME>_<SECONDNAME> $1"; echo "send_photo <FIRSTNAME>_<SECONDNAME> /home/pi/image.jpg"; echo "safe_quit") | ${tgpath}/bin/telegram-cli -k tg-server.pub -W
