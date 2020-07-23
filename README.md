## Json to XML Project.

This project consists of 2 simple Flask applications:
- Sender: Accepts json files as input, converts to XML, encrypts, and sends to Receiver
- Receiver: Accepts encrypted files, decrypts, and stores in XML format.

Usage:
run `docker-compose up --build` from the "Project" directory.

upload json files with:
`curl -X POST -H "Content-Type: application/json" 127.0.0.1:8000/files/<filename> -d @sample.json`

Stored XML files can be seen locally at "Project/receiver/received_files"


### Considerations / Assumptions
Transfer to a remote location: Data is not being transferred to a remote location as both containers are running on the same machine.  However, I included variables for address and host so if they were running on separate hosts, it would be easy to adapt.

I have assumed that both parties share encryption keys and did not generate PKI infrastructure / key exchange for data transfer.