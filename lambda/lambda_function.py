# coding: utf-8
"""
Lambdaの環境変数に登録されているEC2を起動後にサービスを起動する。
EC2は環境変数に複数登録できるようにjson形式をbase64エンコードしたものを使っている。
環境変数はjson_to_env.pyを使って作成。
"""
import json
import os
import base64
import boto3
import time


region = 'ap-northeast-1'


def lambda_handler(event, context):
    # eventの読み込み
    action = event["Action"]  # "Start" or "Stop"

    # 環境変数の読み込み
    json_dict = _fetch_env_dict()
    instance_ids = []  # instance_idsは配列である必要がある。
    for ec2_info in (json_dict):
        instance_ids.append(ec2_info["InstanceId"])

    # Actionに応じてEC2を起動、停止させサービスを起動する。
    ec2_client = boto3.client('ec2', region_name=region)
    response = ec2_client.describe_instances(InstanceIds=instance_ids)
    if (action == "Start"):
        ec2_client.start_instances(InstanceIds=instance_ids)
        # インスタンスの起動を待つ
        # waiter = ec2_client.get_waiter('instance_status_ok')
        # waiter.wait(InstanceIds=instance_ids)
        print("-----Starting-----")
    elif (action == "Stop"):
        ec2_client.stop_instances(InstanceIds=instance_ids)
        return
    else:
        print('Lamdba function could not be executed.')

    # 現在のステータスを表示
    for i, ec2_info in enumerate(json_dict):
        instance_name = ec2_info["InstanceName"]
        ec2_status = response['Reservations'][0]['Instances'][0]['State']['Name']
        print(instance_name + ' is ' + ec2_status + ' now.')

        # コマンドを実行
        print([instance_ids[i]])
        ssm = boto3.client('ssm')
        ssm.send_command(
            InstanceIds=[instance_ids[i]],
            DocumentName="AWS-RunShellScript",
            Parameters={
                "commands": [_get_command(instance_name)]
            }
        )

    return _return_status()


def _fetch_env_dict():
    json_str = base64.b64decode(os.environ['JSON'])
    json_dict = json.loads(json_str)
    return json_dict


def _get_command(instance_name):
    if instance_name == "hoge":
        return "touch hoge"
    elif instance_name == "hogehoge":
        return "touch hogehoge"
    else:
        return "touch default"


def _return_status():
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
