import argparse
from bit import PrivateKey, PrivateKeyTestnet
from bit.network import NetworkAPI, satoshi_to_currency


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Offline Bitcoin Transactions')
    parser.add_argument('--prepare', dest='prepare_transaction', action='store_true',
                        help='Prepare transaction')
    parser.add_argument('--input-address', dest='input_address', type=str,
                        help='Input address')
    parser.add_argument('--output-address', dest='output_address', type=str,
                        help='Output address')
    parser.add_argument('--leftover-address', dest='leftover_address', type=str,
                        help='Leftover address')
    parser.add_argument('--bitcoins', dest='amount', type=str,
                        help='Amount of bitcoins')
    parser.add_argument('--message', dest='message', default='', type=str,
                        help='Transaction message')
    parser.add_argument('--sign', dest='prepared_transaction', type=str,
                        help='Sign prepared transaction (.json)')
    parser.add_argument('--broadcast', dest='signed_transaction', type=str,
                        help='Broadcast signed transaction (.txt)')
    parser.add_argument('--testnet', dest='testnet', action='store_true',
                        help='Use testnet')

    args = parser.parse_args()

    if args.testnet:
        Key = PrivateKeyTestnet
        get_balance = NetworkAPI.get_balance_testnet
    else:
        Key = PrivateKey
        get_balance = NetworkAPI.get_balance

    if args.prepare_transaction:
        input_balance = satoshi_to_currency(get_balance(args.input_address), "btc")
        output_balance = satoshi_to_currency(get_balance(args.output_address), "btc")

        if args.amount == 'ALL':
            outputs = []
            args.leftover_address = args.output_address
            leftover_balance = output_balance
        else:
            outputs = [(args.output_address, float(args.amount), 'btc')]
            if not args.leftover_address:
                args.leftover_address = args.input_address
                leftover_balance = input_balance
            else:
                leftover_balance = satoshi_to_currency(get_balance(args.leftover_address), "btc")

        print('====================================== Prepare Transaction ========================================')
        print(f'Input address:\t\t{args.input_address}', f'\t({input_balance} BTC)')
        print(f'Output address:\t\t{args.output_address}', f'\t({output_balance} BTC)')
        if outputs:
            print(f'Leftover address:\t{args.leftover_address}', f'\t({leftover_balance} BTC)')
        print(f'Send bitcoins:\t\t{args.amount} BTC')
        print('===================================================================================================')

        if args.amount != 'ALL' and float(input_balance) < float(args.amount):
            print('Insufficient input funds!')
            print('===================================================================================================')
            exit(-1)

        """
        transaction = Key.prepare_transaction(args.input_address, outputs, leftover=args.leftover_address,
                                              message=args.message)
        """

        transaction = Key.prepare_transaction(args.input_address, outputs, leftover=args.leftover_address)

        file_name = f'from_{args.input_address}_to_{args.output_address}_{args.amount}_btc.json'
        with open(file_name, 'w') as file:
            file.write(transaction)

        print(f'Prepared transaction: {file_name}')
        print('===================================================================================================')

    if args.prepared_transaction:
        print('======================================== Sign Transaction =========================================')
        print(f'Sign transaction: {args.prepared_transaction}')

        with open(args.prepared_transaction, 'r') as file:
            transaction = file.read()

        input_key = input(f'Enter input key: ').strip()
        transaction = Key(input_key).sign_transaction(transaction)

        file_name = args.prepared_transaction.replace('.json', '.txt')
        with open(file_name, 'w') as file:
            file.write(transaction)

        print('===================================================================================================')
        print(f'Signed transaction: {file_name}')
        print('===================================================================================================')

    if args.signed_transaction:
        print('====================================== Broadcast Transaction ======================================')
        print(f'Broadcast transaction: {args.signed_transaction}')

        with open(args.signed_transaction, 'r') as file:
            transaction = file.read()

        NetworkAPI.broadcast_tx_testnet(transaction)

        print('===================================================================================================')
