import json
import csv
from csv import DictWriter
from web3 import Web3
import pymssql

# In the video, we forget to `install_solc`
# from solcx import compile_standard
from solcx import compile_standard, install_solc
import os
filename="CrudOp_v2.sol"
with open(filename, "r") as file:
    simple_storage_file = file.read()
with open('deploy_details.csv','r') as filez:
            data=filez.read()
            data=data.split('\n')
            latest=len(data)-2
            latest_deploy=(data[latest]).split(',')
            #print(latest_deploy[0])
            owner=latest_deploy[0]
            private_key=latest_deploy[1]
            address=latest_deploy[2]
            filename=latest_deploy[3]
            classname=latest_deploy[4]
#w3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/25211862790c4372abbf918b56ca0c11"))
w3 = Web3(Web3.HTTPProvider("https://eth-ropsten.nownodes.io"))
chain_id = 3
# We add these two lines that we forgot from the video!
print("Installing...")
def newDeploy(version,filename,owner,key):
        install_solc(version)

        # Solidity source code
        compiled_sol = compile_standard(
            {
                "language": "Solidity",
                "sources": {filename: {"content": simple_storage_file}},
                "settings": {
                    "outputSelection": {
                        "*": {
                            "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                        }
                    }
                },
            },
            solc_version=version,
        )

        with open("compiled_code.json", "w") as file:
            json.dump(compiled_sol, file)

        # get bytecode
        bytecode = compiled_sol["contracts"][filename]["UserCrud"]["evm"][
            "bytecode"
        ]["object"]

        # get abi
        abi = json.loads(
            compiled_sol["contracts"][filename]["UserCrud"]["metadata"]
        )["output"]["abi"]

        # w3 = Web3(Web3.HTTPProvider(os.getenv("RINKEBY_RPC_URL")))
        # chain_id = 4
        #
        # For connecting to ganache
        network = "ropsten"
        
        chain_id = 3
        my_address = owner
        private_key = key

        # Create the contract in Python
        SimpleStorage = w3.eth.contract(address=my_address,abi=abi,bytecode=bytecode)
        # Get the latest transaction
        nonce = w3.eth.getTransactionCount(my_address)
        # Submit the transaction that deploys the contract
        transaction = SimpleStorage.constructor().buildTransaction(
            {
                "chainId": chain_id,
                "gasPrice": w3.eth.gas_price,
                "from": my_address,
                "nonce": nonce,
            }
        )
        print("Nonce value : ",nonce)
        # Sign the transaction
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
        print("Deploying Contract!")
        # Send it!
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        # Wait for the transaction to be mined, and get the transaction receipt
        print("Waiting for transaction to finish...")
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Done! Contract deployed to {tx_receipt.contractAddress}")
        #Citizen = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
        #print(Citizen)

        return tx_receipt.contractAddress
def getdeployreceipt():
        
        with open("compiled_code.json", "r") as file:
            data=file.read()
            abi = json.loads(data)
            abi=abi['contracts'][filename][classname]["abi"]
            
            
        #w3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/25211862790c4372abbf918b56ca0c11"))   
        
        nonce = w3.eth.getTransactionCount(owner)
        #address,private_key=deploy_details()
        #print(Citizen,private_key)
        Citizen = w3.eth.contract(address=address, abi=abi)
        return owner,nonce,Citizen
def addUser(certificate,regNo,orgName,name,course):
##        with open('deploy_details.csv','r') as filez:
##            data=filez.read()
##            data=data.split('\n')
##            latest=len(data)-2
##            latest_deploy=(data[latest]).split(',')
##            #print(latest_deploy[0])
##            owner=latest_deploy[0]
##            private_key=latest_deploy[1]
##            address=latest_deploy[2]
##            filename=latest_deploy[3]
##            classname=latest_deploy[4]
        chain_id=3
        owner,nonce,Citizen=getdeployreceipt()
        print(f"Initial Stored Value {Citizen.functions.getUserCount().call()}")
        #print("")
        greeting_transaction = Citizen.functions.insertUser(certificate,regNo,orgName,name,course).buildTransaction(
            {
                "chainId": chain_id,
                "gasPrice": w3.eth.gas_price,
                "from": owner,
                "nonce": nonce ,

            }
        )
        print("JSON data : ",{
                "chainId": chain_id,
                "gasPrice": w3.eth.gas_price,
                "from": owner,
                "nonce": nonce ,

            })
        signed_greeting_txn = w3.eth.account.sign_transaction(
            greeting_transaction, private_key=private_key
        )
        tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
        print("Updating stored Value..."," signed_greeting_txn :",signed_greeting_txn,"  Transaction Hash :",tx_greeting_hash)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)
        #print(tx_receipt)
        print(Citizen.functions.getUserCount().call())

        return tx_receipt.transactionHash
def retrieveBlockDetails():
        
        owner,nonce,Citizen=getdeployreceipt()
        InputCount=Citizen.functions.getUserCount().call()
        print("This is User Count",InputCount)
        data=[]
        for i in range(InputCount):
              print("Info at particular Index",Citizen.functions.getUserAtIndex(i).call())  
              data.append(Citizen.functions.getUserAtIndex(i).call())  
        
        return data
def createDict(data):
        listAttr = ["userCertificate","RegNo","organisation","name","course","hashcode"]
        data_dict={}
        listOutput=[]
        for index in data:
            count=0
        #print(index)
            data_dict={}
            for j in index:

                data_dict[listAttr[count]]=j
            #print(data_dict)
                count=count+1
            listOutput.append(data_dict)
        return listOutput 
from flask import Flask, request, abort,render_template,jsonify
import json
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
server = '198.27.98.137'
user = 'blockchain'
paswd = 'Qazxsw123!@#'
database = 'blockchain'
conn = pymssql.connect(server, user, paswd, database)
cursor,conn=[conn.cursor(),conn]
#count=0
@app.route('/newDeploy')
def deploy_details():
        owner="0xf5465a2CC5378717914E8f31508234e29B485Ed9"
        key="0x8b632208e72458df7d978adb96074e5ba64443d2a2662455a8c2d5a971ba8b42"
        filename="CrudOp_v2.sol"
        version="0.4.22"
        classname="UserCrud"
        deployed_contract=newDeploy(version,filename,owner,key)

        with open("deploy_details.csv",'+a')as f:
            fieldnames=['Owner_Add','Privatekey','DeployedAt','filename','classname']
            data_dict={}    
            data_dict['Owner_Add']= owner
            data_dict['Privatekey']=key
            data_dict['DeployedAt']=deployed_contract 
            data_dict['filename']=filename
            data_dict['classname']=classname
            w =DictWriter(f,fieldnames=fieldnames)
            #w.writeheader()
            w.writerow(data_dict)
            f.close()    
        return deployed_contract,key
@app.route('/retrieveBlockchain')
def blockRetrieve():
        data=retrieveBlockDetails()
        return jsonify(data)
@app.route('/insertUser', methods=['GET','POST'])
def insertUser():
    count=0
    if request.method == 'POST':
        data_dict={}
        print("received data: ", request.data)
        list_bulk_data=request.get_json()
        for json_data in list_bulk_data:
            orgName=""
            count=count+1
            regNo=json_data['holder_id']
            
            name=json_data['holder_name']
            course=json_data['event_name']
            certificate_Id=json_data['cert_no']
        

            try:
                hashCode=addUser(certificate_Id,regNo,orgName,name,course)    
                hashCode=hashCode.hex()
                data= {"status":"1","hashcode":hashCode}
                
                json_data['hash']=hashCode

#            cursor.execute("INSERT INTO dbo.blockchain (userCertificate,RegNo,organisation,name,course,hashcode) VALUES(123,134,'somethn','python','fg','gdsfg');")
         #       cursor.execute("INSERT INTO blockchain (userCertificate,RegNo,organisation,name,course,hashcode,email,mobileNo) VALUES" +"("+str(certificate_Id)+","+str(regNo)+",'"+str(orgName)+"','"+str(name)+"','"+str(course)+"','"+str(hashCode)+"','"+str(email)+"','"+str(mobile)+"');")
          #      conn.commit()
                print("Entry Number :",count)
        #return jsonify(data)
            except Exception as e:
                print("Exception: ",e)
                return jsonify({"status":"0"})
        with open('raw_data.txt','w') as file1:
            file1.write(json.dumps(list_bulk_data))
            file1.close()
        return jsonify(data)    

@app.route('/retrieveUsers',methods=['GET','POST'])
def retrieveUsers():
    cursor.execute("SELECT * FROM "+ str(database))
    data=cursor.fetchall()
    #data=str(data).replace(")","}").replace("(","{")
    #data=str(data).replace("[","{").replace("]","}")
    listOutput=createDict(data)
    return jsonify(listOutput)
@app.route('/certiRoute',methods=['GET','POST'])
def certiRoute():
   # if(request.method=='POST'):
        inputId = request.args.get('id', type = int)
        cursor.execute('SELECT * FROM blockchain WHERE userCertificate='+str(inputId)+';')
        rowDetails=cursor.fetchall()
        final_list=createDict(rowDetails)
        final_dict=final_list[0]
        return jsonify(final_dict)
if __name__=='__main__':
    0
    app.run(host='103.248.60.212',port=9022)
