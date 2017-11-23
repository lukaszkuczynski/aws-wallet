export ROLE=$1
rm wallet_app.zip
pip install -r requirements.txt -t walletapp
cd walletapp
zip -r ../wallet_app.zip *
cd ../
export FILE_PATH=${PWD}/wallet_app.zip
export ES_HOST=$2
./create_lambda.sh $ROLE $FILE_PATH $ES_HOST
