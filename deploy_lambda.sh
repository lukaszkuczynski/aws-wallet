export ROLE=$1
rm wallet.zip
zip -r wallet.zip wallet.py
export FILE_PATH=${PWD}/wallet.zip
./create_lambda.sh $ROLE $FILE_PATH
