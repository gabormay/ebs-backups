# main.tf: Provider and variable definitions
# Copyright (c) 2016 Gabor Maylander (gabormay@github)

# Note that the parameters below are picked up from the following environment variables:
#   AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
# Alternatively, you can have them defined here (not recommended)
provider "aws" {
    # access_key = "..."
    # secret_key = "..."
    # region = "..."
}

