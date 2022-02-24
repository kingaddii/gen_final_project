set -eu

#### CONFIGURATION SECTION ####
stack_name=team5jack
deployment_bucket=gen-team5jack-deployment
#### CONFIGURATION SECTION ####

# Delete deploy dir if exists for a clean start
if [ -d ".deployment" ]; then rm -rf .deployment; fi

# Pip install dependendies from requirements.txt to specific directory
python3 -m pip install --target ./.deployment/dependencies -r requirements.txt


#Use Docker Instead:
#docker run -v "$PWD":/var/task "public.ecr.aws/sam/build-python3.9" /bin/sh -c "pip install -r requirements.txt -t ./.deployment/dependencies; exit"
# Zip all installed dependencies into a deployment package
cd ./.deployment/dependencies
sudo zip -r ../lambda-package.zip .
# Merge 'app' directory with python code into the deployment package zip
cd ../../src
sudo zip -gr ../.deployment/lambda-package.zip app
cd ..


 #aws s3 mb s3://gen-team5jack-deployment
 #aws s3 mb s3://team5jack-cafe-data --profile learner-profile --region eu-west-1

# Package template and upload local resources (deployment package zip) to S3
# A unique S3 filename is automatically generated each time
aws cloudformation package --template-file cloudformation.yml --s3-bucket ${deployment_bucket} --output-template-file .deployment/cloudformation-packaged.yml 

# Deploy template
aws cloudformation deploy --stack-name ${stack_name}-lambda --template-file .deployment/cloudformation-packaged.yml --region eu-west-1 --capabilities CAPABILITY_IAM --parameter-overrides NamePrefix=${stack_name} 