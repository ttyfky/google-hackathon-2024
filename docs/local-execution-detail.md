


## 実行方法

プロジェクトの *ルート* で以下のコマンドを実行してください。b-moz が実行され、サーバーが立ち上がります。

```shell
make run
```

実際の b-moz は Cloud Run 上において、Cloud Pub/Sub や Gemini などの Google Cloud プロダクトとシームレスな連携を行いますが、
ローカル環境における b-moz の実行では環境設定の簡単化のため、以下の条件で実行されます。

1. Pub/Sub とのやり取りなし
2. データストア (デモでは Google Spread Sheet) への書き込みをせず CSV をローカルに保存
   1. 保存先は [resources/temp](../resources/temp/) 

実環境における Google Cloud プロダクトの動的な連携はデモ動画の方でご確認ください。

### API の呼び出し
以下では、API の呼び出し方法を示します。  
jq を用いることで結果が見やすくなりますが、 jq がインストールされていない場合は、`| jq .` の部分を取り除いて実行してください。

### 最新製品のモデル情報の収集

Android の情報収集例
```shell
curl -s -X POST http://localhost:3000/api/v1/collect/catalog/latest  \
-H 'Content-Type: application/json' \
-d '{
  "category": "android"
}' | jq .
```

### 特定のモデルのカタログ情報収集例

Pixel 7 のカタログ情報取得
```shell
curl -s -X POST http://localhost:3000/api/v1/collect/catalog/spec  \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-d '{
  "target": "Pixel 9",
  "category": "smartphone"
}' | jq .
```


iPhone 16 のカタログ情報取得(`mode:SS_SAVE` をペイロードに追加しローカルにCSVを保存)

```shell
curl -s -X POST http://localhost:3000/api/v1/collect/catalog/spec  \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-d '{
  "target": "iPhone16",
  "category": "smartphone",
  "mode": "SS_SAVE"
}' | jq .
```
