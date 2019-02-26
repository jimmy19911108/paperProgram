gnome-terminal -e "redis-server --port 6379"
echo "Signalling server will start in"
echo "3"
sleep 1
echo "2"
sleep 1
echo "1"
sleep 1
clear
./signal.py 192.168.1.98 5000
