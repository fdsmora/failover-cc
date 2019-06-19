# failover-cc

failover code challenge v.1

Programming language: Python 3

Description

It's a web server based system that constist of:
1. A web server called monitor
2. A web server called Primary Application instance
3. A web server called Standby Application instance
4. A client that submits requests to the web server system

It works like this. The client submits http GET or POST requests to the monitor server, which forwards the request to the primary instance. The primary instances process the request and replicates the resulting data to the standby web server. 

Currently only these operations are supported:
1. Update request to the primary
2. 'kill' the primary instance
3. get the status of the data from the primary instance and the standby instance. This is useful for checking that after an 'udpdate' request, the data in the standby is correctly updated. 
4. FAILOVER . If operation 2. is performed, the monitor will detect that primary is down (because it no longer receives heartbeats from the primary) and it will automatically run the failover, causing the standby to become primary, so it starts sending heartbeats to the monitor, processing client requests and replicating this requests to the former primary. 

Pending features to implement:

. Have more than one instance running as primary.

. Load balancing between primary instances.

. Restart 'dead' primary so that it becomes immediately an standby (although code in the monitor is implemented to handle that, only it's pending to implement the code to make dead primary come back to life).

Data in the web servers

The 'update' operation basically is an update of entries in a dictionary data structure that is held in the primary instance and mirrowed in the standby instance. After an update operation in the primary, the operation is replicated immediately to the standby instance. The 'get_state' operation on the standby is useful to verify that this was run successfully. 

Implementation details

The Web servers were implemented using the Python http.server module, which provides very easy and simple HTTTP and web programming capabilities. 

Each web server is run as a separate process within my host. 

Communication between all of these entities is by curl GET and POST HTTP calls. 

Failover design and implementation

Failover works by having the primary instance send periodic heartbeats to the monitor server. As soon as the monitor boots up, it will start checking for heartbeats from the primary. A hearbeat in the monitor is received as an HTTP get with query string parameters: 
1) Name of the server
2) Role, which should be primary
3) Timestamp (epoch) of the heartbeat generation at the primary.

The monitor receives the GET and uses de heartbeat timestamp to update an internal variable. A separate thread in the monitor periodically checks for the age of the last heartbeat received and if it's beyond certain age, then it's considered expired, but will run a number of retries to see if a new heartbeat arrives. If not, then primary is considered to be failed and failover is triggered. These are the steps of failover:

Monitor
1. Updates it's registry by switching the primary to standby and viceversa.
2. Submits a requests for the standby to do failover
3. Starts listening again for heartbeats

Standby
1. Receives a failover request from monitor
2. Updates it's role to be primary and updates it's known standby to be now primary.
3. Starts heartbeating (only the primary heartbeats)

Primary
As it's dead, the only thing that could  happen is that it's restarted. If that happens, it should begin as primary and start sending heartbeats to the monitor. However, after failover, the monitor considers it to be an standby, so if it recieves a heartbeat from it, it will trigger a failover requests so that it becomes standby. The 'restart' of 'dead' primary is pending to implement. 


How to use

1. In a linux terminal, run the 'main.py' script, which will boot the three servers, which start listening for incomming connections immediately. 
2. In a separate terminal, run the 'client' script. For usage, please run 'client -h'. 

Example:

Start the web servers:

[fausto@fausto-lap failover-cc]$ ./main.py
app2(standby):Server up and running
app1(primary):Server up and running
2019-06-19 11:08:35.876237:app1(primary):Starting heartbeating
2019-06-19 11:08:35.876413:app1(primary):heartbeat (server_name:app1, role:primary, timestamp:1560960515876) emitted to localhost:8080
2019-06-19 11:08:35.885889:monitor:heartbeat received: {'server_name': 'app1', 'role': 'primary', 'timestamp': '1560960515876'}
2019-06-19 11:08:36.887949:app1(primary):heartbeat (server_name:app1, role:primary, timestamp:1560960516887) emitted to localhost:8080
2019-06-19 11:08:36.904747:monitor:heartbeat received: {'server_name': 'app1', 'role': 'primary', 'timestamp': '1560960516887'}
2019-06-19 11:08:37.908539:app1(primary):heartbeat (server_name:app1, role:primary, timestamp:1560960517908) emitted to localhost:8080
2019-06-19 11:08:37.923816:monitor:heartbeat received: {'server_name': 'app1', 'role': 'primary', 'timestamp': '1560960517908'}
2019-06-19 11:08:38.925853:app1(primary):heartbeat (server_name:app1, role:primary, timestamp:1560960518925) emitted to localhost:8080
2019-06-19 11:08:38.940343:monitor:heartbeat received: {'server_name': 'app1', 'role': 'primary', 'timestamp': '1560960518925'}
2019-06-19 11:08:39.947144:app1(primary):heartbeat (server_name:app1, role:primary, timestamp:1560960519947) emitted to localhost:8080
2019-06-19 11:08:39.968189:monitor:heartbeat received: {'server_name': 'app1', 'role': 'primary', 'timestamp': '1560960519947'}

Notice that the hearbeats generation from the primary and the monitor receiving the heartbeats. 

Playing with the client:

[fausto@fausto-lap failover-cc]$ ./client -h                                                                                                   [0/469]
usage: client [-h] [-kill-primary] [-update] [-file FILE]
              [-get_state GET_STATE]

client to test the failover code challenge. Please start the system first by
running ./main.py

optional arguments:
  -h, --help            show this help message and exit
  -kill-primary         kills the primary instance
  -update               Updates the entries map in the application instance
                        with the corresponding entires specified in
                        -file=update_file. The -file parameter is required.
                        The keys that can be updated are: id, index, guid,
                        isActive, balance, picture, age, eyeColor, name,
                        about, registered, latitude, longitude. The values can
                        be any string and the entries to be updated have to be
                        each entrie per line and the key separated by an equal
                        sign from the value. This is an example of the
                        contents of 'update_file' where 'id' and 'name'
                        entries are to be updated: id=1234 name=Fernanda The
                        command will print the updated map from the server,
                        which is returned from it.
  -file FILE            File with map that will update
  -get_state GET_STATE  returns the state of the data map in the specified
                        server. Options are 'primary' and 'standby'. This is
                        useful to check if after the update operation in the
                        primary the data was correctly replicated to the
                        standby

Get the current state of the map contained in the primary instance
                   
[fausto@fausto-lap failover-cc]$ ./client -get_state=primary
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  1696    0  1696    0     0   1696      0 --:--:-- --:--:-- --:--:--  331k
b"{'id': '5d06aabffca870c0de76aa79', 'index': '0', 'guid': '8c6af915-c68b-4263-912a-08c56557acc0', 'isActive': 'True', 'balance': '$3,029.87', 'picture': 'http://placehold.it/32x32', 'age': '25', 'eyeColor': 'blue', 'name': 'Cecelia Morgan', 'gender': 'female', 'company': 'VERTON', 'email': 'ceciliamorgan@verton.com', 'phone': '+1 (983) 578-2433', 'address': '523 Miami Court, Starks, Minnesota, 2078', 'about': 'Proident sint ea incididunt et ea ipsum Lorem occaecat nostrud adipisicing elit. Nulla veniam non elit enim magna esse dolore incididunt non velit. Reprehenderit cillum duis reprehenderit nostrud consequat eu sunt ea magna voluptate fugiat eiusmod. Id id reprehenderit in id excepteur. Exercitation ullamco do esse officia quis quis.\\r\\n', 'registered': '2019-01-09T03:13:07 +06:00', 'latitude': '-8.768006', 'longitude': '-103.11563'}"

Get the current state of the map mirrowed in the standby

[fausto@fausto-lap failover-cc]$ ./client -get_state=standby
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  1696    0  1696    0     0   1696      0 --:--:-- --:--:-- --:--:--  331k
b"{'id': '5d06aabffca870c0de76aa79', 'index': '0', 'guid': '8c6af915-c68b-4263-912a-08c56557acc0', 'isActive': 'True', 'balance': '$3,029.87', 'picture': 'http://placehold.it/32x32', 'age': '25', 'eyeColor': 'blue', 'name': 'Cecelia Morgan', 'gender': 'female', 'company': 'VERTON', 'email': 'ceciliamorgan@verton.com', 'phone': '+1 (983) 578-2433', 'address': '523 Miami Court, Starks, Minnesota, 2078', 'about': 'Proident sint ea incididunt et ea ipsum Lorem occaecat nostrud adipisicing elit. Nulla veniam non elit enim magna esse dolore incididunt non velit. Reprehenderit cillum duis reprehenderit nostrud consequat eu sunt ea magna voluptate fugiat eiusmod. Id id reprehenderit in id excepteur. Exercitation ullamco do esse officia quis quis.\\r\\n', 'registered': '2019-01-09T03:13:07 +06:00', 'latitude': '-8.768006', 'longitude': '-103.11563'}"

Prepare for the update of entries 'id' and 'name' in the map

[fausto@fausto-lap failover-cc]$ cat update_file 
id=999
name=Paola

[fausto@fausto-lap failover-cc]$ ./client -update -file=update_file
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   299    0    61  100   238     61    238  0:00:01 --:--:--  0:00:01  4211
b"ACTION: update \n OUT: b'No response from server' \n ERR: None\n"

Show the state of the map after the update in the primary

[fausto@fausto-lap failover-cc]$ ./client -get_state=primary
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  1644    0  1644    0     0   1644      0 --:--:-- --:--:-- --:--:--  401k
b'{\'id\': "\'999\'", \'index\': \'0\', \'guid\': \'8c6af915-c68b-4263-912a-08c56557acc0\', \'isActive\': \'True\', \'balance\': \'$3,029.87\', \'picture\': \'http://placehold.it/32x32\', \'age\': \'25\', \'eyeColor\': \'blue\', \'name\': "\'Paola\'", \'gender\': \'female\', \'company\': \'VERTON\', \'email\': \'ceciliamorgan@verton.com\', \'phone\': \'+1 (983) 578-2433\', \'address\': \'523 Miami Court, Starks, Minnesota, 2078\', \'about\': \'Proident sint ea incididunt et ea ipsum Lorem occaecat nostrud adipisicing elit. Nulla veniam non elit enim magna esse dolore incididunt non velit. Reprehenderit cillum duis reprehenderit nostrud consequat eu sunt ea magna voluptate fugiat eiusmod. Id id reprehenderit in id excepteur. Exercitation ullamco do esse officia quis quis.\\r\\n\', \'registered\': \'2019-01-09T03:13:07 +06:00\', \'latitude\': \'-8.768006\', \'longitude\': \'-103.11563\'}'
[fausto@fausto-lap failover-cc]$ 

Show that the update was replicated to the standby

[fausto@fausto-lap failover-cc]$ ./client -get_state=standby
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  1644    0  1644    0     0   1644      0 --:--:-- --:--:-- --:--:--  321k
b'{\'id\': "\'999\'", \'index\': \'0\', \'guid\': \'8c6af915-c68b-4263-912a-08c56557acc0\', \'isActive\': \'True\', \'balance\': \'$3,029.87\', \'picture\': \'http://placehold.it/32x32\', \'age\': \'25\', \'eyeColor\': \'blue\', \'name\': "\'Paola\'", \'gender\': \'female\', \'company\': \'VERTON\', \'email\': \'ceciliamorgan@verton.com\', \'phone\': \'+1 (983) 578-2433\', \'address\': \'523 Miami Court, Starks, Minnesota, 2078\', \'about\': \'Proident sint ea incididunt et ea ipsum Lorem occaecat nostrud adipisicing elit. Nulla veniam non elit enim magna esse dolore incididunt non velit. Reprehenderit cillum duis reprehenderit nostrud consequat eu sunt ea magna voluptate fugiat eiusmod. Id id reprehenderit in id excepteur. Exercitation ullamco do esse officia quis quis.\\r\\n\', \'registered\': \'2019-01-09T03:13:07 +06:00\', \'latitude\': \'-8.768006\', \'longitude\': \'-103.11563\'}'

Kill the primary instance

[fausto@fausto-lap failover-cc]$ ./client -kill-primary
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    44    0    44    0     0     44      0 --:--:-- --:--:-- --:--:--  2315

Show the state of the primary. There's no connection as it's down. 

[fausto@fausto-lap failover-cc]$ ./client -get_state=primary
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0curl: (7) Failed to connect to localhost port 8081: Connection refused
b''

Show that the standby is still up and running. Failover should automatically engage now but it's to be done. 

[fausto@fausto-lap failover-cc]$ ./client -get_state=standby
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  1644    0  1644    0     0   1644      0 --:--:-- --:--:-- --:--:--  321k
b'{\'id\': "\'999\'", \'index\': \'0\', \'guid\': \'8c6af915-c68b-4263-912a-08c56557acc0\', \'isActive\': \'True\', \'balance\': \'$3,029.87\', \'picture\': \'http://placehold.it/32x32\', \'age\': \'25\', \'eyeColor\': \'blue\', \'name\': "\'Paola\'", \'gender\': \'female\', \'company\': \'VERTON\', \'email\': \'ceciliamorgan@verton.com\', \'phone\': \'+1 (983) 578-2433\', \'address\': \'523 Miami Court, Starks, Minnesota, 2078\', \'about\': \'Proident sint ea incididunt et ea ipsum Lorem occaecat nostrud adipisicing elit. Nulla veniam non elit enim magna esse dolore incididunt non velit. Reprehenderit cillum duis reprehenderit nostrud consequat eu sunt ea magna voluptate fugiat eiusmod. Id id reprehenderit in id excepteur. Exercitation ullamco do esse officia quis quis.\\r\\n\', \'registered\': \'2019-01-09T03:13:07 +06:00\', \'latitude\': \'-8.768006\', \'longitude\': \'-103.11563\'}'


FAILOVER

kill the client

[fausto@fausto-lap failover-cc]$ ./client -kill-primary
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    44    0    44    0     0     44      0 --:--:-- --:--:-- --:--:--   880


Now the system performs failover

2019-06-19 11:09:35.828171:monitor:heartbeat received: {'server_name': 'app1', 'role': 'primary', 'timestamp': '1560960575802'}                       
2019-06-19 11:09:36.836161:app1(primary):heartbeat (server_name:app1, role:primary, timestamp:1560960576836) emitted to localhost:8080                
2019-06-19 11:09:36.856657:monitor:heartbeat received: {'server_name': 'app1', 'role': 'primary', 'timestamp': '1560960576836'}                       
                                                                                                                                                      
app1:ERR:Requested to die. Farewell...                                                                                                                
monitor:EXPIRED hb FROM app1,primary , RETRYING                                                                                                       
monitor:EXPIRED hb FROM app1,primary , RETRYING                                                                                                       
monitor:EXPIRED hb FROM app1,primary , RETRYING                                                                                                       
monitor:Failed to detect recent heartbeat from primary, performing failover...                                                                        
monitor:starting failover                                                                                                                             
app2(primary):Starting as primary
2019-06-19 11:09:50.858149:app2(primary):Starting heartbeating
2019-06-19 11:09:50.858231:app2(primary):heartbeat (server_name:app2, role:primary, timestamp:1560960590858) emitted to localhost:8080
app2:Failover peformed, I am now a primary
monitor:Request to host app2 for failover completed

The heartbeat cycle is resumed

2019-06-19 11:09:50.868356:monitor:heartbeat received: {'server_name': 'app2', 'role': 'primary', 'timestamp': '1560960590858'}
2019-06-19 11:09:51.870470:app2(primary):heartbeat (server_name:app2, role:primary, timestamp:1560960591870) emitted to localhost:8080
2019-06-19 11:09:51.885768:monitor:heartbeat received: {'server_name': 'app2', 'role': 'primary', 'timestamp': '1560960591870'}
2019-06-19 11:09:52.887860:app2(primary):heartbeat (server_name:app2, role:primary, timestamp:1560960592887) emitted to localhost:8080
2019-06-19 11:09:52.902347:monitor:heartbeat received: {'server_name': 'app2', 'role': 'primary', 'timestamp': '1560960592887'}

