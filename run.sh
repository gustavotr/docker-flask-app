docker container rm gcontainer && docker run -d -p 80:80 --name gcontainer gustavoapp
#docker container rm gcontainer && docker run -d --network="host" --name gcontainer gustavoapp