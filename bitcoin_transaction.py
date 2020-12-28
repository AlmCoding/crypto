import argparse
from bit import PrivateKey, PrivateKeyTestnet
from bit.network import NetworkAPI


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Offline Bitcoin Transactions')
    parser.add_argument('--prepare', dest='prepare_transaction', action='store_true',
                        help='Prepare transaction (offline)')
    parser.add_argument('--input-address', dest='input_address', type=str,
                        help='Input address (offline)')
    parser.add_argument('--output-address', dest='output_address', type=str,
                        help='Output address (offline)')
    parser.add_argument('--leftover-address', dest='leftover_address', type=str,
                        help='Leftover address (offline)')
    parser.add_argument('--send-bitcoins', dest='send_bitcoins', type=str,
                        help='Amount of bitcoins (offline)')
    parser.add_argument('--message', dest='message', type=str,
                        help='Transaction message (optional)')
    parser.add_argument('--sign', dest='prepared_transaction', type=str,
                        help='Sign prepared transaction (offline)')
    parser.add_argument('--broadcast', dest='signed_transaction', type=str,
                        help='Broadcast signed transaction (online)')
    parser.add_argument('--use-testnet', dest='use_testnet', action='store_true',
                        help='Use testnet')

    args = parser.parse_args()

    Key = PrivateKeyTestnet if args.use_testnet else PrivateKey

    if args.prepare_transaction:
        
        if args.send_bitcoins == 'ALL':
            args.leftover_address = args.output_address
            outputs = []
        else:
            outputs = [(args.output_address, float(args.send_bitcoins), 'btc')]

        if not args.leftover_address:
            args.leftover_address = args.input_address

        print('====================================== Prepare Transaction ========================================')
        print(f'Input address: {args.input_address}')
        print(f'Output address: {args.output_address}')
        if outputs:
            print(f'Leftover address: {args.leftover_address}')
        print(f'Send bitcoins: {args.send_bitcoins}')
        print('===================================================================================================')

        transaction = Key.prepare_transaction(args.input_address, outputs, leftover=args.leftover_address,
                                              message=args.message)

        file_name = f'from_{args.input_address}_to_{args.output_address}_{args.send_bitcoins}_btc.json'
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

        print(f'Signed transaction: {file_name}')
        print('===================================================================================================')

    if args.signed_transaction:
        print('====================================== Broadcast Transaction ======================================')
        print(f'Broadcast transaction: {args.signed_transaction}')

        with open(args.signed_transaction, 'r') as file:
            transaction = file.read()

        NetworkAPI.broadcast_tx_testnet(transaction)

        # print(f'Transaction hash: {transaction_hash}')
        print('===================================================================================================')
