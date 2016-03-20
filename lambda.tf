resource "aws_lambda_function" "lambda_ebs_backup" {
    filename = "lambda_function_payload.zip"
    function_name = "ebs_backup"
    role = "${aws_iam_role.ebs_backup_role.arn}"
    handler = "lambda_ebs_backup.backup_handler"
    runtime = "python2.7"
    timeout = "30"
}