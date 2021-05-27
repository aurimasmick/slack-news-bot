terraform {

  backend "s3" {
    bucket  = "mano-tf-projects"
    key     = "slack-news-bot/main.tfstate"
    region  = "eu-west-1"
    encrypt = true
  }
}