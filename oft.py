import argparse
from bit import PrivateKey, PrivateKeyTestnet
from bit.network import NetworkAPI, satoshi_to_currency


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Offline Bitcoin Transactions')
    parser.add_argument('--prepare', dest='prepare', action='store_true',
                        help='Prepare transaction (online)')
    parser.add_argument('--sign', dest='sign', type=str,
                        help='Sign transaction (offline)')
    parser.add_argument('--broadcast', dest='broadcast', type=str,
                        help='Broadcast transaction (online)')

    args = parser.parse_args()

    Key = PrivateKeyTestnet if args.testnet else PrivateKey

    if args.prepare:
        print('============================================================================')
        print('======================= Prepare Transaction (Online) =======================')
        print('============================================================================')

        sender_address = input(f'Enter input address: ').strip()
        sender_balance = NetworkAPI.get_balance_testnet(sender_address)
        sender_balance_btc = satoshi_to_currency(sender_balance, 'btc')
        sender_balance_eur = satoshi_to_currency(sender_balance, 'eur')
        print(f'Current balance: {sender_balance_btc} BTC ({sender_balance_eur} €)')
        print('============================================================================')

        receiver_address = input('Enter output address: ').strip()
        amount_btc = float(input('How many bitcoins you want to send (-1 == ALL): ').strip())

        if amount_btc == -1:
            leftover_address = receiver_address
        else:
            leftover_address = input('Enter leftover address (): ').strip()

        print('============================================================================')

        message = input('Message (optional): ')

        outputs = [] if amount_btc == -1 else [(receiver_address, amount_btc, 'btc')]
        transaction = Key.prepare_transaction(sender_address, outputs, leftover=leftover_address, message=message)

    if args.sign:
        pass

    if args.broadcast:
        pass

    b = 12

    exit(0)



        #outputs = [] if amount_btc == -1 else [(receiver_address, amount_btc, 'btc')]
        #params = {'outputs': outputs, 'leftover': leftover_address, 'message': message}


    private_key = input('Enter private key: ')
    private_key = Key(private_key)
    signed_transaction = private_key.sign_transaction(prepared_transaction)
