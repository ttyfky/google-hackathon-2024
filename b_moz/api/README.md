# /api
This api dir if for the b-moz presentation layer.


## collect

Collect api is for collecting catalog information from the web.

- /api/v1/collect/catalog/latest
  - Collect the latest catalog information from the web. 
    - body: {"category": "android"}
  - This publishes the collected information to the pubsub that is used in the following APIs.
- /api/v1/collect/catalog/spec
  - Collect the specific catalog information for given target from the web.
    - body: {"target": "pixel 8", category: "smartphone"} 
  - By default, the collected information is pushes to the pubsub.
  - If you want to save the information to the spreadsheet, you should include `mode` field as `SS_SAVE` in the payload.
- /api/v1/collect/catalog/spec/pubsub
  - Collect the specific catalog information from the web by pubsub.
- /api/v1/collect/catalog/spec/pubsub/save
  - Save the specific catalog information from the web, that are in the pubsub.


```mermaid
sequenceDiagram
    participant Scheduler
    participant LATEST as /catalog/latest
    participant PSL as PubSub for latest 
    participant SPECPS as /catalog/spec/pubsub
    participant PSC as PubSub for catalog 
    participant SAVE as /catalog/spec/pubsub/save

    Scheduler ->> LATEST: 新モデル収集トリガー
    LATEST ->> PSL: 新モデルリスト
    Scheduler ->> SPECPS: 新モデルの仕様収集トリガー
    SPECPS ->> PSL: モデル Pull
    PSL -->> SPECPS: 新モデル名
    SPECPS ->> SPECPS: 処理
    SPECPS ->> PSC: カタログ情報
    Scheduler ->> SAVE: 保存トリガー
    SAVE -> PSC: カタログ Pull
    PSC -->> SAVE: katarogu 
    SAVE ->> SAVE: 処理
    SAVE ->> DataStore: 保存
 

```
