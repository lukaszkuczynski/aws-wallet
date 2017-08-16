AWS_USER=$1

aws lambda invoke \
--invocation-type RequestResponse \
--function-name HelloAws \
--region eu-central-1 \
--log-type Tail \
--payload '{"first_name":"Lukasz", "last_name":"Kuczyński"}' \
--profile $AWS_USER \
aws_output.txt

echo "invoking lambda produces result"
cat aws_output.txt