# Sendgrid Manage Teammates

Sendgridのチームメート管理を楽にするスクリプト。  
以下の処理が実行される。

1. 状態確認
2. 招待中のチームメートを全削除
3. 削除対象チームメートを削除
4. 新規招待対象のチームメートを招待
5. 状態確認

`data/users.json`、`data/roles.json`でチームメートとパーミッションを定義するが、定義したものと一致したかはチェックしていないため実行時に出力されるログで目検チェックする必要がある。

## サブユーザの切り替え

`.env`に`env`を定義。もしくはスクリプトを実行する際に`export env=xxx`の様にする。

## users.json

`data/`配下に配置する。  
サブユーザ単位で変更する場合は`data/<hoge>/`の配下にそれぞれ配置する。

```sh
[
    {
        "email": "example@example.com",
        "is_admin": "true",
        "role": "Administrator",
        "state": "present" # present or absent
    },
    {
        "email": "example+hoge@example.com",
        "is_admin": "false",
        "role": "DeveloperReadOnly",
        "state": "present"
    }
]

```

## roles.json

`data/`配下に配置する。  
サブユーザ単位で変更する場合は`data/<hoge>/`の配下にそれぞれ配置する。
