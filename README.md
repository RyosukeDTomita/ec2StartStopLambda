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
1. 起動したいインスタンスの名前とidをenv.jsonに設定し、[json_to_env.py](./json_to_env.py)を実行して得た結果をクリップボードにコピーする。
2. AWS Lambdaから、環境変数にコピーした値を設定。
3. テストタブに移動し、eventを指定して実行する。
   
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

# PREPARING

