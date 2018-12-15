# Pre Requisite
- `python 3`
- AWS Cli Configured with credentials ( For more info, See https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)
    Note: This configuration is used for creating role, uploading lambda function and creating a bucket. This is not required at code run time.

# Create virtual environment

`pip install virtualenv`

`virtualenv -p python3 virt`

`source virt/bin/activate`

# Install  Python Dependencies

`pip install -r requirements.txt`

# Configure Constants

Edit `config.py` file to change constants.

# Setup Python Package for lambda

Following script builds the package and uploads the python package to the lambda. It also creates the role, with required permissions and S3 bucket

`sh setup.sh`


# How to use.
This lambda function can be used to
