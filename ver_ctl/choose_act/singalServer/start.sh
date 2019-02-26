gnome-terminal -e "redis-server --port 6379"
gnome-terminal -e "redis-server --port 6380"
echo "Signalling server will start in"
echo "3"
sleep 1
echo "2"
sleep 1
echo "1"
sleep 1
clear
./signal.py 127.0.0.1 5000
