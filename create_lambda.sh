aws lambda create-function \
--region eu-central-1 \
--function-name HelloAws \
--zip-file fileb://$2 \
--role $1  \
--handler wallet.my_handler \
--runtime python3.6 \
--timeout 15 \
--memory-size 512
