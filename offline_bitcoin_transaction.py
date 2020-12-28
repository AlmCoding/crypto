from bit import PrivateKey, PrivateKeyTestnet
from get_logger import get_logger

from bit import PrivateKeyTestnet
from bit.network import NetworkAPI, satoshi_to_currency


# documentation for bit library: https://ofek.dev/bit/index.html
########################################################################################################################
use_testnet = True
########################################################################################################################
private_key = 'cQ32ujxLKq897Qt84ucVamXrCQU7GWaMQ7QxtLhYrqoGVN5Vurgp'
address = ''
amount_btc = 0.001                                                   # use -1 to transfer all available funds
receiver_address = 'mhroD6fvireqUstD3WQYUc1TkSVL9MY1Fk'              # amount will be moved to this address
leftover_address = 'n49Ro1Z8qsaBkwiW8ACHb8mgY4VYru5SpV'              # unspent coins will be moved to this address
message = 'optional'
########################################################################################################################



satoshi_to_currency(NetworkAPI.get_balance_testnet(address), 'eur')


tx_data = PrivateKeyTestnet.prepare_transaction(address, [('n2eMqTT929pb1RDNuqEnxdaLau1rxy3efi', 1, 'jpy')])



if __name__ == '__main__':
    log = get_logger('output.txt', __name__)
    log.info('#==========================================================================#')



    if len(private_key) != 52:
        log.error("The 'private_key' is invalid!")
        exit(-1)
    elif len(receiver_address) != 34:
        log.error("The 'receiver_address' is invalid!")
        exit(-1)
    elif len(leftover_address) != 34:
        log.error("The 'leftover_address' is invalid!")
        exit(-1)
    elif amount_btc == -1 and receiver_address != leftover_address:
        log.error("When moving all funds the 'receiver_address' and the 'leftover_address' must be the same!")
        exit(-1)

    Key = PrivateKeyTestnet if use_testnet else PrivateKey
    private_key = Key(private_key)
    balance_btc = float(private_key.get_balance('btc'))
    log.info(f'Version: {private_key.version}')
    log.info(f'Address: {private_key.address}')
    log.info(f'Balance: {balance_btc}')

    if not balance_btc or (balance_btc - amount_btc) <= 0.0:
        log.error('The private key has insufficient funds!')
        exit(-1)

    outputs = [] if amount_btc == -1 else [(receiver_address, amount_btc, 'btc')]
    params = {'outputs': outputs, 'leftover': leftover_address, 'message': message}

    if sign_offline:
        transaction = private_key.create_transaction(**params)
        file_name = f'from_{private_key.address}_to_{receiver_address}_{amount_btc}_btc.txt'
        with open(file_name, 'w') as file:
            file.write(transaction)


    else:
        transaction_hash = private_key.send(**params)
        log.info(f'Transaction: {transaction_hash}')

    a = 12


"""    
    if amount_btc == -1:
        # Spent all funds
        transaction_hash = private_key.send([], leftover=receiver_address, message=message)
    else:
        # Spend funds partly
        transaction_hash = private_key.send([(receiver_address, amount_btc, 'btc')],
                                            leftover=leftover_address, message=message)
"""

