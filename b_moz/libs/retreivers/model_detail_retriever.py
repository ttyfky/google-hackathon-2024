from typing import List

from langchain.schema import Document
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.retrievers import BaseRetriever


class ModelSpecDocRetriever(BaseRetriever):

    def __init__(self):
        super().__init__()

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        # TODO: Implement the logic to retrieve the relevant documents for the given query.
        return [Document(page_content=_temp_iphone15)]


_temp_iphone15 = """
仕上げ
ブラック

ブルー

グリーン

イエロー

ピンク

アルミニウムのデザイン、Ceramic Shieldの前面、カラーインフューズドガラスの背面

容量1
128GB

256GB

512GB

サイズと重量2
幅： 71.6 mm

高さ： 147.6 mm

厚さ： 7.80 mm

重量： 171 g

ディスプレイ
Super Retina XDRディスプレイ

6.1インチ（対角）オールスクリーンOLEDディスプレイ

2,556 x 1,179ピクセル解像度、460ppi

Dynamic Island

HDRディスプレイ

True Tone

広色域（P3）

触覚タッチ

2,000,000:1コントラスト比（標準）

最大輝度1,000ニト（標準）、ピーク輝度1,600ニト（HDR）、ピーク輝度2,000ニト（屋外）

耐指紋性撥油コーティング

複数の言語と文字の同時表示をサポート

iPhone 15のディスプレイは、美しい曲線を描くように四隅に丸みを持たせてデザインされており、標準的な長方形に収まります。標準的な長方形として対角線の長さを測った場合のスクリーンのサイズは6.12インチです（実際の表示領域はこれより小さくなります）。

防沫性能、耐水性能、防塵性能3
IEC規格60529にもとづくIP68等級（最大水深6メートルで最大30分間）

チップ
A16 Bionicチップ

2つの高性能コアと4つの高効率コアを搭載した6コアCPU

5コアGPU

16コアNeural Engine

カメラ
先進的なデュアルカメラシステム

48MPメイン：26mm、ƒ/1.6絞り値、センサーシフト光学式手ぶれ補正、100% Focus Pixels、超高解像度の写真（24MPと48MP）に対応

12MP超広角：13mm、ƒ/2.4絞り値と120°視野角

12MPの2倍望遠（クアッドピクセルセンサーを活用）：52mm、ƒ/1.6絞り値、センサーシフト光学式手ぶれ補正、100% Focus Pixels

2倍の光学ズームイン、2倍の光学ズームアウト、4倍の光学ズームレンジ

最大10倍のデジタルズーム

サファイアクリスタル製レンズカバー

True Toneフラッシュ

Photonic Engine

Deep Fusion

スマートHDR 5

フォーカス機能と被写界深度コントロールが使える次世代のポートレート

6つのエフェクトを備えたポートレートライティング

ナイトモード

パノラマ（最大63MP）

フォトグラフスタイル

写真とLive Photosの広色域キャプチャ

レンズ補正（超広角）

高度な赤目修正

自動手ぶれ補正

バーストモード

写真へのジオタグ添付

画像撮影フォーマット：HEIF、JPEG

ビデオ撮影
4Kビデオ撮影（24fps、25fps、30fpsまたは60fps）

1080p HDビデオ撮影（25fps、30fpsまたは60fps）

720p HDビデオ撮影（30fps）

シネマティックモード（最大4K HDR、30fps）

アクションモード（最大2.8K、60fps）

ドルビービジョン対応HDRビデオ撮影（最大4K、60fps）

1080pスローモーションビデオ（120fpsまたは240fps）に対応

手ぶれ補正機能を使ったタイムラプスビデオ

ナイトモードのタイムラプス

QuickTakeビデオ

ビデオのセンサーシフト光学式手ぶれ補正（メイン）

最大6倍のデジタルズーム

オーディオズーム

True Toneフラッシュ

映画レベルのビデオ手ぶれ補正（4K、1080p、720p）

連続オートフォーカスビデオ

4Kビデオの撮影中に8MPの静止画を撮影

再生ズーム

ビデオ撮影フォーマット：HEVC、H.264

ステレオ録音

TrueDepthカメラ
12MPカメラ

ƒ/1.9絞り値

Focus Pixelsを使ったオートフォーカス

Retina Flash

Photonic Engine

Deep Fusion

スマートHDR 5

フォーカス機能と被写界深度コントロールが使える次世代のポートレート

6つのエフェクトを備えたポートレートライティング

アニ文字とミー文字

ナイトモード

フォトグラフスタイル

写真とLive Photosの広色域キャプチャ

レンズ補正

自動手ぶれ補正

バーストモード

4Kビデオ撮影（24fps、25fps、30fpsまたは60fps）

1080p HDビデオ撮影（25fps、30fpsまたは60fps）

シネマティックモード（最大4K HDR、30fps）

ドルビービジョン対応HDRビデオ撮影（最大4K、60fps）

1080pスローモーションビデオ（120fps）に対応

手ぶれ補正機能を使ったタイムラプスビデオ

ナイトモードのタイムラプス

QuickTakeビデオ

映画レベルのビデオ手ぶれ補正（4K、1080p、720p）

Face ID
TrueDepthカメラによる顔認識の有効化

Apple Pay
Face IDを使った、店頭、アプリ内、ウェブ上でのiPhoneによる支払い

Mac上でのApple Payによる購入の完了

iPhoneに入れたSuica、PASMO、ICOCAによる電車などの交通機関の利用、店頭での購入

エクスプレスカードによる交通機関の支払い4

Apple Payについてさらに詳しく

安全のための機能
緊急SOS

衝突事故検出5

携帯電話/ワイヤレス通信方式
モデルA3089* モデルA3093*

5G NR（バンドn1、n2、n3、n5、n7、n8、n12、n14、n20、n25、n26、n28、n29、n30、n38、n40、n41、n48、n53、n66、n70、n71、n75、n76、n77、n78、n79）

FDD-LTE（バンド1、2、3、4、5、7、8、11、12、13、14、17、18、19、20、21、25、26、28、29、30、32、66、71）

TD-LTE（バンド34、38、39、40、41、42、46、48、53）

UMTS/HSPA+/DC-HSDPA（850、900、1,700/2,100、1,900、2,100MHz）

GSM/EDGE（850、900、1,800、1,900MHz）

全モデル

4x4 MIMO対応5G（sub-6 GHz）6

4x4 MIMOとLAA対応ギガビットLTE6

2x2 MIMO対応Wi-Fi 6（802.11ax）

Bluetooth 5.3

第2世代の超広帯域チップ7

リーダーモード対応NFC

予備電力機能付きエクスプレスカード

FeliCa

5GおよびLTE対応の詳細については通信事業者にお問い合わせください。apple.com/jp/iphone/cellularもあわせてご覧ください。

位置情報
GPS、GLONASS、Galileo、QZSS、BeiDou

デジタルコンパス

Wi-Fi

携帯電話通信

iBeaconマイクロロケーション

ビデオ通話8
携帯電話ネットワークまたはWi-Fi経由でのFaceTimeビデオ通話

5GまたはWi-Fi経由でのFaceTime HD（1080p）ビデオ通話

SharePlayを使って映画、テレビ番組、音楽やアプリの体験をFaceTime通話で共有

画面共有

FaceTimeビデオでのポートレートモード

空間オーディオ

「声を分離」と「ワイドスペクトル」のマイクモード

バックカメラでのズーム

オーディオ通話8
FaceTimeオーディオ

Voice over LTE（VoLTE）6

SharePlayを使って映画、テレビ番組、音楽やアプリの体験をFaceTime通話で共有

画面共有

空間オーディオ

「声を分離」と「ワイドスペクトル」のマイクモード

オーディオ再生
AAC、MP3、Apple Lossless、FLAC、ドルビーデジタル、ドルビーデジタルプラス、ドルビーアトモスなどのフォーマットに対応

空間オーディオ再生

ユーザーによる設定が可能な最大音量制限

ビデオ再生
HEVC、H.264、ProResなどのフォーマットに対応

HDR（ドルビービジョン、HDR10、HLG）

Apple TV（第2世代以降）またはAirPlay対応スマートテレビへの、最大4K HDRのAirPlayミラーリング、写真、ビデオ出力

対応するビデオミラーリングとビデオ出力：USB-C経由のDisplayPort出力（標準対応）またはUSB-C Digital AVアダプタ（モデルA2119、アダプタは別売り）経由で最大4K HDR9

Siri10
メッセージの送信やリマインダーの設定などをあなたの声で実行

「Hey Siri」を使ってあなたの声だけでハンズフリーで起動

よく使うアプリのショートカットをあなたの声で実行

Siriについてさらに詳しく

本体のボタンとコネクタ
音量を上げる/下げる

着信/消音

サイドボタン

USB-Cコネクタ

内蔵マイク

内蔵ステレオスピーカー

充電と拡張性
USB-Cコネクタで以下に対応：

充電

DisplayPort

USB 2（最大480Mb/s）

電源とバッテリー11
ビデオ再生: 最大20時間

ビデオ再生（ストリーミング）: 最大16時間

オーディオ再生: 最大80時間

リチャージャブルリチウムイオンバッテリー内蔵

最大15WのMagSafeワイヤレス充電12

最大15WのQi2ワイヤレス充電12

最大7.5WのQiワイヤレス充電12

高速充電に対応：約30分で最大50%充電13（別売りの20W以上のアダプタを使用）

MagSafe
最大15Wのワイヤレス充電12

マグネットアレイ

アラインメントマグネット

アクセサリ識別NFC

磁力計

センサー
Face ID

気圧計

ハイダイナミックレンジジャイロ

高重力加速度センサー

近接センサー

デュアル環境光センサー

オペレーティングシステム
iOS

iOSは世界で最もパーソナルで安全なモバイルオペレーティングシステムです。パワフルな機能の数々が詰め込まれていて、あなたのプライバシーを守れるように設計されています。

iOS の新機能を見る

アクセシビリティ
iPhoneを最大限に活用できるように、視覚、身体機能、聴覚、認知の障がいのある方をサポートするアクセシビリティ機能を内蔵しています。

アクセシビリティ についてさらに詳しく

アクセシビリティ機能：

VoiceOver

ズーム

拡大鏡

音声コントロール

スイッチコントロール

AssistiveTouch

クローズドキャプション

パーソナルボイス

ライブスピーチ

Siriにタイプ入力

読み上げコンテンツ

内蔵アプリ
Apple Store

App Store

ブック

計算機

カレンダー

カメラ

Clips

時計

コンパス

連絡先

FaceTime

ファイル

探す

フィットネス

フリーボード

GarageBand

ヘルスケア

ホーム

iMovie

iTunes Store

Keynote

拡大鏡

メール

マップ

計測

メッセージ

ミュージック

メモ

Numbers

Pages

電話

写真

ポッドキャスト

リマインダー

Safari

設定

ショートカット

Siri

株価

ヒント

翻訳

TV

ボイスメモ

ウォレット

Watch

天気

SIMカード
デュアルSIM（nano-SIMとeSIM）14

デュアルeSIMに対応14

eSIMについてさらに詳しく

海外旅行中のeSIMの利用についてさらに詳しく

補聴器両立性の格付け
M3、T4

対応するメール添付ファイル
表示可能なドキュメントの種類

.jpg、.tiff、.gif（画像） .doc、.docx（Microsoft Word） .htm、.html（ウェブページ） .key（Keynote） .numbers（Numbers） .pages（Pages） .pdf（プレビュー、Adobe Acrobat） .ppt、.pptx（Microsoft PowerPoint） .txt（テキスト） .rtf（リッチテキストフォーマット） .vcf（連絡先情報） .xls、.xlsx（Microsoft Excel） .zip、.ics、.usdz（USDZ Universal）

システム条件
Apple ID（一部の機能に必要）

インターネットアクセス15

MacまたはWindowsパソコンとの同期には以下が必要：

macOS Catalina 10.15以降（Finderを使用）

macOS High Sierra 10.13からmacOS Mojave 10.14.6まで（iTunes 12.8以降を使用）

Windows 10以降（iTunes 12.12.10以降を使用、apple.com/jp/itunesから無料でダウンロード可能）

動作環境
動作時環境温度： 0°〜35°C

保管時（非動作時）温度： -20°〜45°C

相対湿度： 5%〜95%（結露しないこと）

動作高度： 3,048mまでテスト済み
"""
