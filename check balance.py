from web3 import Web3
import requests
import json

TokenAddress = input('Enter contract address: ')
url_eth = "https://api.bscscan.com/api"
bsc = 'https://bsc-dataseed.binance.org/'
web3 = Web3(Web3.HTTPProvider(bsc))

contract_address = web3.toChecksumAddress(TokenAddress)
API_ENDPOINT = url_eth+"?module=contract&action=getabi&address="+str(contract_address)
r = requests.get(url=API_ENDPOINT)
response = r.json()
abi = json.loads(response["result"])

contract = web3.eth.contract(address=contract_address, abi=abi)
totalSupply = contract.functions.totalSupply().call()
symbol = contract.functions.symbol().call()

print(f"Total supply: {web3.fromWei(totalSupply, 'ether'):.2f}")
print(f'Name: {contract.functions.name().call()}')
print(f'Symbol: {symbol}')
total_bnb = 0


with open('addresses.txt', 'r') as file:
    all_address = file.readlines()

for MyAddress in all_address:
    MyAddress = MyAddress.replace('\n', '')
    total_bnb += web3.fromWei(web3.eth.get_balance(MyAddress), 'ether')
    address = web3.toChecksumAddress(MyAddress)
    balance = contract.functions.balanceOf(address).call()
    print(f"{MyAddress}: {web3.fromWei(balance, 'ether'):.2f} {symbol},"
          f" {web3.fromWei(web3.eth.get_balance(MyAddress), 'ether'):.2f} BNB")

print(total_bnb)

input()
