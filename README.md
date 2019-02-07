# Handle CloudWatch Events and post to Slack


# Install / Update
1. Create a Slack application `AWS Notifications`.
2. Get the slack token from `AWS Notifications`.
3. Create/Update the `.env.yml` file with the token.
```bash
$ cat .env.yml
lambda:
  environment:
    SLACK_API_TOKEN: "xoxa-11111111111-1111111111111-1111111111111-abcd3abcd3abcd3abcd3abcd3abcd3123"
    SLACK_CHANNEL: "aws-notifications"
```
4. Setup python venv and install modules for local development.
```bash
virtualenv -p `which python3` venv
source venv/bin/activate
pip install -U -r requirements.txt
```
5. Install/Update the infrastructure.
```bash
npm install serverless -g

# It needs to be Installed local
npm install serverless-python-requirements

sls deploy <--aws-profile my-rt-profile>  --stage prod
```
