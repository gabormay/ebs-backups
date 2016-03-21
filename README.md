# EBS Backups 
Scheduled backups of EBS volumes using Lambda - provisioned via Terraform

# Prerequisites
* Install [Terraform](https://www.terraform.io/downloads.html)
* Have `zip` available on the PATH


# Usage
* Make sure to have your AWS credentials set up properly. Normally these are picked up from the following standard environment 
variables: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` and `AWS_DEFAULT_REGION`. Alternatively, you can enter these parameters directly in `main.tf` but this is not recommended.
* (optional) Review and adjust the schedule and the backup retention policies in `lambda.tf` and `lambda_ebs_backup.py`
* Run the following commands to provision the lambda function to AWS:
    * `./build.sh`
    * (optional) `terraform plan`
    * `terraform apply`

# Cleaning up
Run `terraform destroy` to clean up and delete all associated resources from AWS. Note that this needs the `terraform.tfstate` that was created during the provisioning step above.

# Known limitations, TODOs
* AWS Lambda requires the function package to be uploaded as a zip file. However, Terraform does not provide any support in creating a zip file yet, hence we need the extra 'build' step. 
* Currently the backup schedule as well as the backup retention policies are hard-wired into the code. A possible improvement would be to have them configurable.

