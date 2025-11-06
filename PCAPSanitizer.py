from scapy.all import PcapReader, PcapWriter
from scapy.all import packet
from scapy.layers.inet import IP, defragment
import os

# Assortment of functions used to inspect PCAP files & determine if they are useful for our dataset

def peekPacket(PCAPFile):
    if not os.path.exists(PCAPFile):
        print("File not found")
        return -1
        
    with PcapReader(PCAPFile) as reader:
        for pkt in reader:
            try:
                print(pkt.show2())
                return
            except Exception:
                print("Packet exception")
                return -1


def seekPacket(PCAPFile, num=0):
    if not os.path.exists(PCAPFile):
        print("File not found")
        return -1
        
    with PcapReader(PCAPFile) as reader:
        for i, pkt in enumerate(reader):
            if i == num:
                try:
                    return pkt.show2(dump=True)
                except Exception:
                    print(f"Packet exception at {i}")
                    continue
            elif i > num:
                # Sanity check to ensure corruption does not lead to EOF exception
                print("Packet skipped, possible corruption")
                break
            else:
                continue

def verifyFile(PCAPFile):
    #Ensures all traffic is TCP/UDP
    #UDP Fragments NOT handled
    if not os.path.exists(PCAPFile):
        print("File not found")
        return -1

    count = 0
    with PcapReader(PCAPFile) as reader:
        for i, pkt in enumerate(reader):
            if pkt.haslayer("TCP") or pkt.haslayer("UDP"):
                continue
            else:
                print(f"Packet {i} neither TCP/UDP {pkt.summary()}")
                count += 1
                continue

    return count

def seperateFragments(PCAPFile, PCAPFileOut):
    #Obtains all UDP fragments and attempts reassembly
    #Appends all to a new pcap file
    if not os.path.exists(PCAPFile):
        print("File not found")
        return -1
        
    frags = []

    with PcapReader(PCAPFile) as reader:
        for pkt in reader:
            if IP in pkt:
                ip = pkt[IP]
                if ip.proto == 17 and (ip.flags.MF or ip.frag > 0):
                    frags.append(ip)
    reassemble = defragment(ip)
    print(f'{len(reassemble)} packets reassembled, writing out')

    with PcapWriter(PCAPFileOut, append=False, sync=True) as writer:
        for pkt in reassemble:
            writer.write(pkt)
    return 0


def __main__():
    file = input("Please enter an ABSOLUTE file path to a PCAP file: ")
    if not os.path.exists(file):
        print("File not found")
        return -1
    else:
        while True:
            print("1: Peek Packet\n2: Seek Packet\n3: Verify File\n4: Separate Fragments\n5: Exit")
            choice = input("Please enter your choice: ")
            if choice == '1':
                peekPacket(file)
            elif choice == '2':
                num = int(input("Enter packet number to seek: "))
                result = seekPacket(file, num)
                if result != -1:
                    print(result)
            elif choice == '3':
                count = verifyFile(file)
                if count != -1:
                    print(f"File verification complete, {count} non-TCP/UDP packets found.")
            elif choice == '4':
                outFile = input("Enter output PCAP file path: ")
                seperateFragments(file, outFile)
            elif choice == '5':
                break
            else:
                print("Invalid option.")


if __name__ == "__main__":
    __main__()