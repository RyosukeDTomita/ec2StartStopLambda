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


region = 'ap-northeast-1'


def lambda_handler(event, context):
    # eventの読み込み
    action = event["Action"]  # "Start" or "Stop"

    # 環境変数の読み込み
    json_dict_list = _fetch_env_dict()
    # 引数InstanceIdsは配列である必要があるためinstanceIDの配列を作成
    instance_ids = []
    for ec2_info in (json_dict_list):
        instance_ids.append(ec2_info["InstanceId"])

    # テストケース(Start, Stop)に基いてインスタンスを起動、停止
    ec2_client = boto3.client('ec2', region_name=region)
    response = ec2_client.describe_instances(InstanceIds=instance_ids)

    if (action == "Start"):
        ec2_client.start_instances(InstanceIds=instance_ids)
        print("-----Starting-----")
        # インスタンス起動を待つ
        waiter = ec2_client.get_waiter('instance_status_ok')
        waiter.wait(InstanceIds=instance_ids)
        # インスタンスのステータスを出力する。
        _print_instances_status(response)
    elif (action == "Stop"):
        ec2_client.stop_instances(InstanceIds=instance_ids)
        print("-----Stopping-----")
        return _return_status()
    else:
        print('imvalid action')

    # インスタンスごとに個別のサービスを起動する。
    for i, ec2_info in enumerate(json_dict_list):
        # 現在のステータスを表示
        instance_name = ec2_info["InstanceName"]
        print(f"{instance_name} service start")

        # コマンドを実行
        print([instance_ids[i]])
        ssm = boto3.client('ssm')
        ssm.send_command(
            InstanceIds=[instance_ids[i]],
            DocumentName="AWS-RunShellScript",
            Parameters={
                "commands": _get_command(instance_name)
            }
        )

    return _return_status()


def _fetch_env_dict() -> dict:
    """_summary_
    lambdaの環境変数をjsonとして。取り出す。

    Returns:
        dict: インスタンス名をキーにしたinstanceID
    """
    json_str = base64.b64decode(os.environ['JSON'])
    json_dict_list = json.loads(json_str)
    return json_dict_list


def _get_command(instance_name) -> list:
    """_summary_
    インスタンス名をもとに適切なサービス起動コマンドを返す。

    Args:
        instance_name (str): インスタンス名

    Returns:
        list: サービスの起動コマンドのリスト
    """
    if instance_name == "instance1":
        return [
            "touch instance1"
        ]
    elif instance_name == "instance2":
        return [
            "touch instance2"
        ]
    # DBサーバ
    elif instance_name == "instance3":
        return [
            "touch instance3"
        ]
    else:
        return ["touch default"]  # default test command


def _print_instances_status(response: list):
    """_summary_
    インスタンスのステータスを確認する

    Args:
        response (list): インスタンス起動の結果が入っているやつ
    """
    for r in response['Reservations']:
        instance_id = r['Instances'][0]['InstanceId']
        status = r['Instances'][0]['State']['Name']
        print(f"{instance_id} is {status}")


def _return_status():
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
