# INDEX

- [ABOUT](#ABOUT)
- [ENVIRONMENT](#ABOUT)
- [PREPARING](#PREPARING)
- [HOW TO USE](#HOW-TO-USE)
- [REFERENCE](#REFERENCE)

# ABOUT
インスタンスの起動自動化を行い，コマンドを自動実行する

# ENVIRONMENT
- python 3.10
- AWS Lambda

# HOW TO USE
## EC2側の設定
1. EC2インスタンスを作成する。**AmazonSSMManagedInstanceCore**を持ったIAMロールをアタッチする。
2. SSM経由で接続できることを確認する。

## Lambda側の設定
1. Lambda関数を作成する。**AmazonEC2ReadOnlyAccess**，**AmazonSSMFullAccess**，カスタマーインラインポリシーをつけたIAMロールをアタッチする。
2. 起動したいインスタンスの名前とidをenv.jsonに設定し、[json_to_env.py](./json_to_env.py)を実行して得た結果をクリップボードにコピーする。
3. AWS Lambdaから、環境変数にコピーした値を設定。
4. テストタブに移動し、eventを指定して実行する。

```json
// カスタマーインラインポリシー
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:Describe*",
                "ec2:Start*",
                "ec2:Stop*"
            ],
            "Resource": "*"
        }
    ]
}
```

```json
{
  "Action": "Start"
}
```

```json
{
  "Action": "Stop"
}
```

# REFERENCE
- [EC2インスタンスをLambdaから起動する](https://qiita.com/YK0214/items/59bc0e5ae89f68af74b3)
- [環境変数をJSONで保存する](https://dev.classmethod.jp/articles/aws-lambda-env-var-json/)
- [lambdaでコマンドを実行する際のsleep](https://qiita.com/yakkuru/items/0b61cfb80bc30c00ac91)
- [IAMの設定](https://qiita.com/high5/items/dbc32ffb07b603bbf709)

# PREPARING
