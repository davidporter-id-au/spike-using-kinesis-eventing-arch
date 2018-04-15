#!/bin/bash -eu
cd $(dirname $0)

streamArn=$(aws cloudformation describe-stacks --stack-name temp-stream --query 'Stacks[0].Outputs[?OutputKey == `StreamArn`] | [0].OutputValue' --output text)

aws cloudformation deploy \
		--template-file deploy.out.yml \
		--capabilities CAPABILITY_IAM \
		--stack-name "temp-stream-lambda-reader" \
		--parameter-overrides \
			StreamArn="$streamArn" \
			RuntimeRoleArn='arn:aws:iam::000000000000:*' \
			ForwardingStreamName='SomeStream' \
			RoleToAssume='arn:aws:iam::000000000000:role/temp-stream-CrossAccountAssumedRole-XXXXXXXXXX'
