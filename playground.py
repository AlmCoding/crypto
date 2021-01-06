from bit import PrivateKeyTestnet

my_key = PrivateKeyTestnet()
print(my_key.version)
print('Key:\t\t', my_key.to_wif())
print('Address:\t', my_key.address)
