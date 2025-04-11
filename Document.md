
Deploy Chaincode
./network.sh up createChannel -s couchdb

'''bash
./network.sh deployCC -ccn basic -ccp ../asset-transfer-basic/chaincode-javascript -ccl javascript
'''

./network.sh deployCC -ccn ledger -ccp ../asset-transfer-ledger-queries/chaincode-javascript/ -ccl javascript -ccep "OR('Org1MSP.peer','Org2MSP.peer')"


## Run Socket Server

'''bash
python main.py
'''

## Run Client in raspberry pi
'''bash
python edge.py
'''

### Frontend

'''bash
npm run dev
'''

### Backend facial recognition service

'''bash
python sural.py
'''

