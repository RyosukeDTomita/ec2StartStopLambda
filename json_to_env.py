# coding: utf-8
"""
lambdaの環境変数には,が使えないらしいのでbase64を挟んでjsonを環境変数に変更する。
本スクリプトはjsonをlambdaに保存できる環境変数の形に変更して出力する。

* サンプル
[
  {
    "InstanceName": "hoge",
    "InstanceId": "i-0xxxxxxxxxx"
  },
  {
    "InstanceName": "fuga",
    "InstanceId": "i-zzzzzzzzzzz"
  }
]
"""
import os
import base64


def _read_json(json_file):
    """_summary_
    jsonファイルを読み込み、文字列として返す。
    jsonモジュール等を使わずにプレーンファイルとして読み込むのは後ほどこれをBase64でエンコードするため。
    改行文字は環境変数として保存する時に邪魔になりそうなので消しておく。

    Args:
        json_file (str): file_path

    Returns:
        str: file_content
    """
    with open(json_file) as f:
        json_str = f.read().replace("\n", "")
    return json_str


def _to_env(json_str):
    """_summary_
    base64を使ってLambdaの環境変数に保存可能な形に変更する。

    Args:
        json_str (str): json_content

    Returns:
        str: lambda env
    """
    return base64.b64encode(json_str.encode("utf-8"))


def main():
    """_summary_
    1. リポジトリ配下にあるenv.jsonを編集
    2. env.jsonをプレーンファイルとして読み込む。
    3. 
    """
    json_file = os.path.join(os.path.dirname(__file__), "env.json")
    json_str = _read_json(json_file)
    lambda_env = _to_env(json_str)
    print(lambda_env.decode('utf-8'))  # copy me and paste it lambda env


if __name__ == "__main__":
    main()
