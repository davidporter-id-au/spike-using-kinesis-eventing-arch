SHELL := /bin/bash

clean:
	@rm *.zip 2> /dev/null || true
	@rm deploy.out.yml 2> /dev/null || true

ensure-bucket-present:
	@$(eval bucketName=$(shell echo "$$(aws sts get-caller-identity --query Account --output text)-lambda-artifacts"))
	@echo ensuring "$(bucketName)" is present
	@aws s3 ls $(bucketName) &> /dev/null || aws s3 mb s3://$(bucketName)

# package up the lambda and upload it to S3
package: clean ensure-bucket-present
	@zip -9 -r --junk-paths ./handler.zip src/*.py
	aws cloudformation package \
		--template-file deploy.sam.yml \
		--output-template-file deploy.out.yml \
		--s3-bucket $(bucketName)
.PHONY: package

deploy: package
	./deploy.sh

.PHONY: deploy

