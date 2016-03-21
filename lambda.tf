# lambda.tf: Sets up the Lambda function and the corresponding schedule
# Copyright (c) 2016 Gabor Maylander (gabormay@github)

resource "aws_lambda_function" "lambda_ebs_backup" {
    filename = "lambda_function_payload.zip"
    function_name = "ebs_backup"
    role = "${aws_iam_role.ebs_backup_role.arn}"
    handler = "lambda_ebs_backup.backup_handler"
    runtime = "python2.7"
    timeout = "30"
}

resource "aws_cloudwatch_event_rule" "every_working_day_at0314" {
    name = "every_working_day_at0314"
    description = "Fires every working day at 3:14am"
    schedule_expression = "cron(14 3 ? * MON-FRI *)"
}

resource "aws_cloudwatch_event_target" "run_backup_every_day" {
    rule = "${aws_cloudwatch_event_rule.every_working_day_at0314.name}"
    target_id = "lambda_ebs_backup"
    arn = "${aws_lambda_function.lambda_ebs_backup.arn}"
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_backup" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = "${aws_lambda_function.lambda_ebs_backup.function_name}"
    principal = "events.amazonaws.com"
    source_arn = "${aws_cloudwatch_event_rule.every_working_day_at0314.arn}"
}