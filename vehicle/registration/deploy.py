from solcx import compile_standard, install_solc
import json
from web3 import Web3, exceptions
import os

from dotenv import load_dotenv

load_dotenv()

with open("Register.sol", "r") as file:
    register_file = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"Register.sol": {"content": register_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled-sol.json", "w") as file:
    json.dump(compiled_sol, file)

bytecode = compiled_sol["contracts"]["Register.sol"]["VehicleContract"]["evm"][
    "bytecode"
]["object"]

abi = json.loads(
    compiled_sol["contracts"]["Register.sol"]["VehicleContract"]["metadata"]
)["output"]["abi"]

contract_id, contract_interface = compiled_sol.popitem()


# Web3 to connect to ganache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337
my_address = "0x945A761933FC807c92431c62dD8b5BFB0B048455"
private_key = os.getenv("PRIVATE_KEY")


# Making Contract
Register = w3.eth.contract(abi=abi, bytecode=bytecode)

# getting latest transaction which is also nonce
nonce = w3.eth.getTransactionCount(my_address)

def deployContract(Register):
    global nonce
    transaction = Register.constructor().buildTransaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": my_address,
            "nonce": nonce,
        }
    )
    nonce += 1
    # 2. Signing the Transaction
    signedTxn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

    # 3. Sending Signed Transaction
    txnHash = w3.eth.send_raw_transaction(signedTxn.rawTransaction)

    # Waiting for confirmation/receipt
    txnReceipt = w3.eth.wait_for_transaction_receipt(txnHash)

    return txnReceipt


contract_address = "0xfb5B5d71D53F6eD6310Bd7579faf6087312C5d2C"

if contract_address == "":
    txnReceipt = deployContract(Register)
    print(txnReceipt.contractAddress)
    register = w3.eth.contract(address=txnReceipt.contractAddress, abi=abi)
    print("Contract Deployed!")
else:
    register = w3.eth.contract(address=contract_address, abi=abi)
    print("Contract Deployed!")


def storeInfo(register, uniqueID, vehicleNo, modelName, vehicleColor, fName, lName, adhaar, dob, gender, email, mobileNo):
    global nonce
    try:
        store_transaction = register.functions.storeInfo(
            uniqueID, vehicleNo, modelName, vehicleColor, fName, lName, adhaar, dob, gender, email, mobileNo
        ).buildTransaction(
            {
                "chainId": chain_id,
                "gasPrice": w3.eth.gas_price,
                "from": my_address,
                "nonce": nonce,
            }
        )

        nonce += 1
        signed_store_txn = w3.eth.account.sign_transaction(
            store_transaction, private_key=private_key
        )
        send_store_txn = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
        tx_store_receipt = w3.eth.wait_for_transaction_receipt(send_store_txn)
        return {"success": True, "data": "Data Entered Successfully!"}

    except exceptions.SolidityError as err:
        return {"success": False, "data": err}


def getOwnerInfoFromAdhaar(register, adhaar):
    global nonce
    try:
        data = register.functions.getOwnerInfoFromAdhaar(adhaar).call()
        return {"success": True, "data": data}
    except exceptions.SolidityError as err:
        return {"success": False, "data": err}

def getVehicleInfoFromUniqueID(register, uniqueID):
    global nonce
    try:
        data = register.functions.getVehicleInfoFromUniqueID(uniqueID).call()
        return {"success": True, "data": data}
    except exceptions.SolidityError as err:
        return {"success": False, "data": err}

def getVehiclesFromAdhaar(register, adhaar):
    global nonce
    try:
        data = register.functions.getVehiclesFromAdhaar(adhaar).call()
        return {"success": True, "data": data}
    except exceptions.SolidityError as err:
        return {"success": False, "data": err}

def getOwnersFromUniqueID(register, uniqueID):
    global nonce
    try:
        data = register.functions.getOwnersFromUniqueID(uniqueID).call()
        return {"success": True, "data": data}
    except exceptions.SolidityError as err:
        return {"success": False, "data": err}

def updateOwnerInfo(register, fName, lName, adhaar, dob, gender, email, mobileNo):
    global nonce
    try:
        store_transaction = register.functions.updateOwnerInfo(
            fName, lName, adhaar, dob, gender, email, mobileNo
        ).buildTransaction(
            {
                "chainId": chain_id,
                "gasPrice": w3.eth.gas_price,
                "from": my_address,
                "nonce": nonce,
            }
        )

        nonce += 1
        signed_store_txn = w3.eth.account.sign_transaction(
            store_transaction, private_key=private_key
        )
        send_store_txn = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
        tx_store_receipt = w3.eth.wait_for_transaction_receipt(send_store_txn)
        return {"success": True, "data": "Data Updated Successfully!"}

    except exceptions.SolidityError as err:
        return {"success": False, "data": err}

def updateVehicleInfo(register, uniqueID, vehicleNo, modelName, vehicleColor):
    global nonce
    try:
        store_transaction = register.functions.updateVehicleInfo(
            uniqueID, vehicleNo, modelName, vehicleColor
        ).buildTransaction(
            {
                "chainId": chain_id,
                "gasPrice": w3.eth.gas_price,
                "from": my_address,
                "nonce": nonce,
            }
        )

        nonce += 1
        signed_store_txn = w3.eth.account.sign_transaction(
            store_transaction, private_key=private_key
        )
        send_store_txn = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
        tx_store_receipt = w3.eth.wait_for_transaction_receipt(send_store_txn)
        return {"success": True, "data": "Data Updated Successfully!"}

    except exceptions.SolidityError as err:
        return {"success": False, "data": err}

while True:
    ip = int(input())
    if ip == 0:
        print(
            storeInfo(
                register,
                '1', '1', 'Santro', 'Blue', 'Sparsh', 'Gupta', '862525352732', '01-10-2010', 'Male', 'sparshtgupta@gmail.com', '7426463647',
            )
        )
    elif ip == 1:
        print(getOwnerInfoFromAdhaar(register, '862525352732'))
    elif ip == 2:
        print(getVehicleInfoFromUniqueID(register, '1'))
    elif ip == 3:
        print(getVehiclesFromAdhaar(register, '862525352732'))
    elif ip == 4:
        print(getOwnersFromUniqueID(register, '1'))
    elif ip == 5:
        print(
            updateOwnerInfo(
                register,
                'Spaaarrsshh', 'Guupta', '862525352732', '01-10-2011', 'Female', 'sparseefhtgupta@gmail.com', '74264636888',
            )
        )
    elif ip == 6:
        print(
            updateVehicleInfo(
                register,
                '1', '2', 'Santro2', 'Blue2'
            )
        )
    elif ip == 7:
        break
    else:
        continue
