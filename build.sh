# build.sh: Builds the upload package for the lambda function 
# Copyright (c) 2016 Gabor Maylander (gabormay)

# This is extremly simple as we have only a single source file
zip lambda_function_payload.zip lambda_ebs_backup.py
