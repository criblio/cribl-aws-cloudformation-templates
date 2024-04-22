This Cloudformation template will create an IAM role in your AWS account that will trust the Cribl Cloud service and setup permissions to your S3 buckets. Two S3 buckets will also be created for this lab to simulate an Amazon Security Lake and a SIEM.
1. Log into your AWS Console, then click here to deploy the cloudformation template. This template will create IAM Policy, Role, and S3 buckets.
2. Click Next and then enter the (account number) that is part of copied arn in previous step and paste it in the account placeholder for both CriblSearchCloudTrust and CriblStreamCloudTrust, update the External ID to 123456.
   ![Step1](https://cribl.awsworkshop.io/images/cribl48.png)
4. Click Next and then click the checkbox at bottom of screen and then click Submit .
   
6. Once the CloudFormation completes, click on the Resources tab to view the name of S3 buckets and the CriblTrustCloud RoleName.
![Step2](https://cribl.awsworkshop.io/images/cribl56.png)

## Artifacts Created
* s3DefaultSecurityLake - This is the S3 bucket that will simulate the Amazon Security Lake destination.
* s3DefaultSIEM - This is the S3 bucket that will mimic a SIEM destination.
* CriblTrustCloud - the IAM Role which will be used to authenticate Cribl Stream to send data and search it.
