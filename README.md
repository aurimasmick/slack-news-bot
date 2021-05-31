# Slack News Bot
Slack bot which posts highest ranked Hacker News and/or Product Hunt articles to Slack at a specific time each day. More information and step by step tutorial how to create bot can be found in [this](https://medium.com/@aurimasmic/how-to-create-a-slack-news-bot-using-aws-lambda-and-terraform-db3ca025b9db) Medium post.

![Alt text](images/slack_message.png?raw=true "Slack Message")

## Architecture
The architecture of this bot is very straightforward. AWS EventBridge  runs on cron like schedule and triggers Lambda function at a set time. The Lambda queries Hacker News and/or Product Hunt API, filters top posts, formats text, and sends to the Slack channel. All AWS resources are deployed with Terraform.

![Alt text](images/newsbot.png?raw=true "Architecture")

### Technologies used
- [terraform-aws-lambda](https://github.com/terraform-aws-modules/terraform-aws-lambda) Terraform module to build Lambda package and provision AWS resources.
- Python asyncio to query large number of URLs (Hacker News).
- Python requests to query GraphQL API (Product Hunt).
- pytest and Github Actions to run AWS Lambda unit tests.
- Slack blocks to format messages.

## Deployment
- set up Slack channel to get token
- create Product Hunt account to get Product Hunt API token (Optional)
- create S3 bucket to store Terraform state and modify `state.tf` file
- export secrets
```
export TF_VAR_slack_bot_token=XXX
export TF_VAR_ph_api_token=XXX
```
- deploy with Terraform
```
terraform init
terraform plan
terraform apply
```
Check [this](https://medium.com/@aurimasmic/how-to-create-a-slack-news-bot-using-aws-lambda-and-terraform-db3ca025b9db) Medium post for step by step guide.


## Modify function
```
python3 -m venv venv
source venv/bin/activate
pip install -r src/slacknewsbot/requirements.txt
```
### Run tests
```
make tests
```
### Makefile functions
```
make deploy
make deploy-with-secrets-file
```