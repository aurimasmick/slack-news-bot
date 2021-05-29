variable "name" {
  description = "Project name"
  type        = string
}
variable "slack_channel_name" {
  description = "The name of the Slack channel where messages are posted"
  type        = string
}
variable "slack_bot_token" {
  description = "Slack bot token to post to channel"
  type        = string
  sensitive   = true
}
variable "post_hn" {
  description = "Controls whether to post Hacker News top stories"
  type        = string
}
variable "post_ph" {
  description = "Controls whether to post Product Hunt top stories. If set to true, need to specify value for ph_api_token variable"
  type        = string
}
variable "ph_api_token" {
  description = "Product Hunt API token. Need to specify value by exporting environment variable or using secrets.tfvars"
  type        = string
  sensitive   = true
  default     = ""
}
variable "stories_number" {
  description = "Number of stories to post to Slack"
  type        = string
}
variable "schedule_expression" {
  description = "Lambda trigger event schedule expression based on cron syntax"
  type        = string
}
