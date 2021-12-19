from aocd import data
from functools import reduce

# data = 'EE00D40C823060'

# Can't use binary number because Python treats it as infinite. Need to use binary string instead
# Make sure to left-pad
message = ''.join([bin(int(x, 16))[2:].zfill(4) for x in data])

versions = 0

def parsepacket(packet: str) -> tuple[any, str]: # Return result and bits consumed
    global versions
    # Get the version - first 3 bits
    version = int(packet[0:3], 2)
    versions += version
    type = int(packet[3:6], 2)
    match type:
        case 4:
            return parseliteral(version, packet, type)
        case _:
            return parseoperator(version, packet, type)

def parseliteral(version: int, packet: str, type: int) -> tuple[int, int]: # Return result and bits consumed
    # print('Literal packet, version', version, packet)
    bin_num = ''
    ind = '1'
    consumed = 6 # Version and type
    while ind == '1':
        ind = packet[consumed]
        bin_num += packet[consumed+1:consumed+5]
        consumed += 5

    return (int(bin_num, 2), consumed)

def parseoperator(version: int, packet: str, type: int) -> tuple[any, str]: # Return result and bits consumed
    # print('Operator packet', type, 'version', version, packet)
    ltype = packet[6]
    consumed = 7 # Version, type, and ltype
    subresults: list[any] = []
    if ltype == '0':
        length = int(packet[consumed:consumed+15], 2) # Total length of packets
        if length > len(packet) - consumed:
            raise Exception('Subpackets size ' + str(length) + ' too big for packet ' + str(len(packet) - consumed))
        consumed += 15
        targetconsumed = consumed + length
        while consumed < targetconsumed:
            # Read a packet
            (result, used) = parsepacket(packet[consumed:])
            subresults.append(result)
            # See how much was consumed
            consumed += used
        
    elif ltype == '1':
        subs = int(packet[consumed:consumed+11], 2) # Number of subpackets
        consumed += 11
        while subs:
            (result, used) = parsepacket(packet[consumed:])
            subresults.append(result)
            consumed += used
            subs -= 1
    else:
        raise 'Invalid length ID type ' + ltype
    
    # Calculate result
    match type:
        case 0:
            res = sum(subresults)
        case 1:
            res = reduce(lambda a,b: a*b, subresults, 1)
        case 2:
            res = min(subresults)
        case 3:
            res = max(subresults)
        case 5:
            res = int(subresults[0] > subresults[1])
        case 6:
            res = int(subresults[0] < subresults[1])
        case 7:
            res = int(subresults[0] == subresults[1])
    
    return (res, consumed)

(res, cons) = parsepacket(message)
print(versions)
print(res)