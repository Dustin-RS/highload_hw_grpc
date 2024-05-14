## Installation
``````
pip install -r requirements.txt
``````
On windows:
````
.\gen.bat
````
On Linux:
````
chmod +x gen.sh
.\gen.sh
````
All tasks in separate terminals

run redis server

``````
docker pull redis
docker run -p 6379:6379 --name redis-server -d redis
``````
Run server
``````
python server.py
``````
First client
``````
python client.py
``````
Second client
``````
python client.py
``````
And so on