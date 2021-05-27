provider "aws" {
  region = "eu-west-1"
}


module "lambda_function" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "2.2.0"

  function_name = var.name
  description   = "Function to post popular articles to Slack"
  handler       = "app.lambda_handler"
  runtime       = "python3.8"
  timeout       = 30

  source_path = "./src/slacknewsbot"

  environment_variables = {
    SLACK_CHANNEL   = var.slack_channel_name
    SLACK_BOT_TOKEN = var.slack_bot_token
    QUERY_HN        = var.query_hn
    QUERY_PH        = var.query_ph
    PH_API_TOKEN    = var.ph_api_token
    STORIES_NUMBER  = var.stories_number
  }
  allowed_triggers = {
    PostToSlack = {
      principal  = "events.amazonaws.com"
      source_arn = aws_cloudwatch_event_rule.cw_cron.arn
    }
  }
  create_current_version_allowed_triggers = false

  tags = {
    Name = var.name
  }
}

# EVENT CONFIG
resource "aws_cloudwatch_event_rule" "cw_cron" {
  name        = "${name}-lambda-trigger"
  description = "Lambda trigge to post to Slack"

  schedule_expression = "cron(0 13 * * ? *)"
}

resource "aws_cloudwatch_event_target" "trigger_slack" {
  rule = aws_cloudwatch_event_rule.cw_cron.name
  arn  = module.lambda_function.lambda_function_arn
}
