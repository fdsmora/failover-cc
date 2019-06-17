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

Unfortunately I ran out of time before implementing the 'failover' and the 'load balancing' features. 

Data in the web servers

The 'update' operation basically is an update of entries in a dictionary data structure that is held in the primary instance and mirrowed in the standby instance. After an update operation in the primary, the operation is replicated immediately to the standby instance. The 'get_state' operation on the standby is useful to verify that this was run successfully. 

Implementation details

The Web servers were implemented using the Python http.server module, which provides very easy and simple HTTTP and web programming capabilities. 

Each web server is run as a separate process within my host. 

Communication between all of these entities is by curl GET and POST HTTP calls. 

How to use

1. In a linux terminal, run the 'main.py' script, which will boot the three servers, which start listening for incomming connections immediately. 
2. In a separate terminal, run the 'client' script. For usage, please run 'client -h'. 

Example:

Start the web servers:

[fausto@fausto-lap failover-cc]$ ./main.py 
Mon Jun 17 02:40:05 2019 standby:ApplicationServer UP - localhost:8082
SUCCESSFULLY REGISTERED
prim: localhost:8081
stby: localhost:8082
Mon Jun 17 02:40:05 2019 MonitorServer UP - localhost:8080
Mon Jun 17 02:40:05 2019 primary:ApplicationServer UP - localhost:8081

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



