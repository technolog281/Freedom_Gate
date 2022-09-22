import ping3


def socket_test(ip_adr: str, port: int):
    ping_test = ping3.ping(ip_adr, unit='ms')

    
    return ping_test


print(socket_test('203.28.9.108', 80))
