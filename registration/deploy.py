from solcx import compile_standard, install_solc
import json
from web3 import Web3, exceptions
import os

from dotenv import load_dotenv

load_dotenv()
install_solc('0.6.0')
with open("./registration/Register.sol", "r") as file:
    register_file = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"Register.sol": {"content": register_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                },
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


# Web3 to connect to infura
w3 = Web3(Web3.HTTPProvider(os.getenv("HTTP_PROVIDER")))
chain_id = 4
my_address = os.getenv("MY_ADDRESS")
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


contract_address = os.getenv('CONTRACT_ADDRESS')

if contract_address == "":
    txnReceipt = deployContract(Register)
    print(txnReceipt.contractAddress)
    register_contract = w3.eth.contract(address=txnReceipt.contractAddress, abi=abi)
    print("Contract Deployed!")
else:
    register_contract = w3.eth.contract(address=contract_address, abi=abi)
    print("Contract Deployed!")


def storeInfo(register_contract, uniqueID, vehicleNo, modelName, vehicleColor, fName, lName, aadhar, dob, userID, ownerInfo2):
    global nonce
    try:
        store_transaction = register_contract.functions.storeInfo(
            uniqueID, vehicleNo, modelName, vehicleColor, fName, lName, aadhar, dob, userID, ownerInfo2
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
        print("Data Entered Successfully!")
        return {"success": True, "data": "Data Entered Successfully!"}

    except exceptions.SolidityError as err:
        return {"success": False, "data": err}


def storeFirInfo(register_contract, uniqueID, firNo, district, year, reason):
    global nonce
    try:
        store_transaction = register_contract.functions.storeFirInfo(
            uniqueID, firNo, district, year, reason
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
        print("FIR Data Entered Successfully!")
        return {"success": True, "data": "FIR Data Entered Successfully!"}

    except exceptions.SolidityError as err:
        return {"success": False, "data": err}

def getFirInfoFromFirNo(register_contract, firNo):
    global nonce
    try:
        data = register_contract.functions.getFirInfoFromFirNo(firNo).call()
        return {"success": True, "data": data}
    except exceptions.SolidityError as err:
        return {"success": False, "data": err}


def getOwnerInfoFromAadhar(register_contract, aadhar):
    global nonce
    try:
        data = register_contract.functions.getOwnerInfoFromAadhar(aadhar).call()
        return {"success": True, "data": data}
    except exceptions.SolidityError as err:
        return {"success": False, "data": err}

def getVehicleInfoFromUniqueID(register_contract, uniqueID):
    global nonce
    try:
        data = register_contract.functions.getVehicleInfoFromUniqueID(uniqueID).call()
        return {"success": True, "data": data}
    except exceptions.SolidityError as err:
        return {"success": False, "data": err}

def getVehiclesFromAadhar(register_contract, aadhar):
    global nonce
    try:
        data = register_contract.functions.getVehiclesFromAadhar(aadhar).call()
        return {"success": True, "data": data}
    except exceptions.SolidityError as err:
        return {"success": False, "data": err}

def getOwnersFromUniqueID(register_contract, uniqueID):
    global nonce
    try:
        data = register_contract.functions.getOwnersFromUniqueID(uniqueID).call()
        return {"success": True, "data": data}
    except exceptions.SolidityError as err:
        return {"success": False, "data": err}

def getAadharfromUserId(register_contract, userID):
    global nonce
    try:
        data = register_contract.functions.getAadharfromUserId(userID).call()
        return {"success": True, "data": data}
    except exceptions.SolidityError as err:
        return {"success": False, "data": err}

def isOwner(register_contract, aadhar):
    global nonce
    try:
        data = register_contract.functions.isOwner(aadhar).call()
        return {"success": True, "data": data}
    except exceptions.SolidityError as err:
        return {"success": False, "data": err}

def isVehicle(register_contract, uniqueID):
    global nonce
    try:
        data = register_contract.functions.isVehicle(uniqueID).call()
        return {"success": True, "data": data}
    except exceptions.SolidityError as err:
        return {"success": False, "data": err}

def updateOwnerInfo(register_contract, fName, lName, aadhar, dob, gender, email, mobileNo):
    global nonce
    try:
        store_transaction = register_contract.functions.updateOwnerInfo(
            fName, lName, aadhar, dob, gender, email, mobileNo
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

def updateVehicleInfo(register_contract, uniqueID, vehicleNo, modelName, vehicleColor):
    global nonce
    try:
        store_transaction = register_contract.functions.updateVehicleInfo(
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