# EBS Backups 
Scheduled backups of EBS volumes using Lambda - provisioned via Terraform

# Known limitations, TODOs
* AWS Lambda requires the function package to be uploaded as a zip file. However, Terraform does not provide any support in creating a zip file yet, hence we need the extra 'build' step. 
* Currently the backup schedule as well as the backup retention policies are hard-wired into the code. A possible improvement would be to have them configurable.

