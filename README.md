# google-hackathon-2024
このレポジトリは 2024 Google Cloud Japan AI Hackathon のためのものです。 

## b-moz

プロダクトの名前は b-moz です。これは、Belong の 百舌鳥 (モズ) を意図しています。  
百舌鳥 は獲物を狩り、木に貯蔵する収集する習性を持っている鳥であることから、
b-moz は製品のカタログ情報を収集し、情報を使いやすい形で保存することを期待して名付けられました。

### Project Setup

ローカル環境で b-moz を実行可能にするための手順を以下に示します。

#### Python 環境
b-moz を実行するためには以下の環境が必要です。
- Python 3.11
  - asdf がある場合には、`asdf install` をルートディレクトリで実行することで必要な Python を取得できます。
- Poetry
  - [公式ドキュメント](https://python-poetry.org/docs/)に従いインストールしてください
  - Mac で Homebrew を利用している場合、`brew install poetry` でインストールできます

#### Google Cloud
b-moz は Google Cloud のサービスを利用しています。
まずは以下の手順で Google Cloud SDK をインストールしてください。
1. [Google Cloud SDK のインストール](https://cloud.google.com/sdk/docs/install) に従い gcloud をインストール
2. `gcloud init` を実行してプロジェクトを選択
3. `gcloud auth application-default login` を実行して ADC を作成

次に上記で設定したプロジェクトに於いて以下を行ってください。

1. Vertex AI における Gemini を利用可能にする
2. Vertex AI User など、Google Cloud のプロダクトを用いるための適切な権限を自身のアカウントに付与

#### Google Custom Search Engine
b-moz は Google Custom Search Engine を利用して製品情報を収集します。
以下の手順で Google Custom Search Engine を作成してください。

1. [Google Custom Search Engine](https://cse.google.com/cse/) にアクセス
2. `Add` をクリックして利用する検索エンジンを作成
3. `検索エンジン ID` 欄にある値を取得
   1. `resources/secrets/.env` ファイルに `GOOGLE_CSE_ID` として記載
4. [CSE](https://developers.google.com/custom-search/v1/introduction?hl=ja) の `キーを取得する` ボタンから、適切なプロジェクトと紐づいた API キーを取得
   1. `resources/secrets/.env` ファイルに `GOOGLE_API_KEY` として記載

#### Initialization
以下のコマンドを実行してください。Poetry をはじめとしたプロジェクトの設定が完了します。
```shell
make setup
```

[secrets](./resources/secrets) ディレクトリにある `.env` ファイルに以下の情報を記載してください。
[.env_example](./resources/secrets/.env.example) が参考になります。

- GOOGLE_CLOUD_PROJECT: Gemini を利用するための Google Cloud のプロジェクト名
- GOOGLE_CSE_ID: Google Custom Search Engine の ID
- GOOGLE_API_KEY: Google Custom Search Engine の API キー

### 実行方法
*リポジトリのルート* で以下のコマンドを実行してください。b-moz が実行され、サーバーが立ち上がります。

```shell
make run
```

実行の詳細、及び API 呼び出し方法に関しては [API の呼び出し](./docs/local-execution-detail.md) を参照してください。
