
from hashlib import sha256
from bit import PrivateKeyTestnet

my_key = PrivateKeyTestnet()
print(my_key.version)
print(my_key.to_wif())
print(my_key.address)
print(my_key.get_balance('btc'))


reciever_key = PrivateKeyTestnet('cThLhxeNA9DsL5KQzk5YM9RPbsB1UoZGrDtgTCvHbFEyFT4Y3nqM')
print(reciever_key.version)
print(reciever_key.to_wif())
print(reciever_key.address)
print(reciever_key.get_balance('btc'))

btc_price = 19000
fee = abs(float(reciever_key.get_balance('btc')) - float(my_key.get_balance('btc'))) * btc_price
print(fee)

tx_hash = my_key.send([(reciever_key.address, 0.001, 'btc')], leftover=reciever_key.address, fee=80, message='stupid leftover transaction')
print(tx_hash)

a1 = ('n49Ro1Z8qsaBkwiW8ACHb8mgY4VYru5SpV', 'cQ32ujxLKq897Qt84ucVamXrCQU7GWaMQ7QxtLhYrqoGVN5Vurgp')
a2 = ('mhroD6fvireqUstD3WQYUc1TkSVL9MY1Fk', 'cRfDYoD2ehhqS4oYS9PMHuddLqq3xpVXJk6jUNndk3cx6xTRosM6')
