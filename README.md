# Sendgrid Manage Teammates

Sendgridのteammates管理を楽にするスクリプト。  

## できること

1. teammateのinviteができる。
    * invite対象のユーザが既にinvite中だった場合はinviteを削除して再度inviteを行う。
    * 事前に定義したpermissionのリストをroleとして指定できる。
2. teammateのdeleteができる。
3. teammateの状態を出力することができる。
    * consoleに標準出力される。
    * invite中のユーザも一緒に出力される。

## サブユーザの切り替え

`.env`に`env`を定義。もしくはスクリプトを実行する際に`export env=xxx`の様にする。

## roles.json

`data/`配下に配置する。  
サブユーザ単位で変更する場合は`data/<hoge>/`の配下にそれぞれ配置する。

## 運用イメージ

* 実施タイミング：月次
    * inviteについては必要があれば随時

1. invite機能を使用して対象のユーザをinviteする。
2. teammatesの一覧を出力する。
3. gitにcommitする。

## 運用の例外等

* roleで設定しているpermissionの変更が発生した場合、既存teammatesの権限はWebUIから手動で変更する。
    * 今回はpermissionの更新機能を含めないため。
* 実施タイミングを月次としているが更新が発生するタイミングでユーザの一覧を更新する。
