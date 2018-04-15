#!/bin/bash -e

stream=$(aws cloudformation describe-stacks \
	--stack-name temp-stream \
	--query 'Stacks[0].Outputs[?OutputKey == `Stream`] | [0].OutputValue' \
	--output text)

while true; do
	sleep 1
	aws kinesis put-record  \
		--stream-name $stream \
		--data "some-record-$(date +%s)" \
		--partition-key test-data \
		--partition-key "akey"
done
