

## Create virtualenv
```
python3 -m venv venv
source venv/bin/activate
pip install -r src/slacknewsbot/requirements.txt
```

## Run tests
```
make tests
```

## Deploy function
### Export secrets
export TF_VAR_slack_bot_token=XXX
export TF_VAR_ph_api_token=XXX
### Deploy
```
make deploy
```
### Deploy with secrets file
```
make deploy-with-secrets-file
```