# 在庫管理システム

リアルタイム在庫管理とChatWork通知機能を備えた在庫管理アプリケーションです。

## 機能

- 📦 リアルタイム在庫管理
- 🔄 ボタンクリックによる在庫数の増減
- ⚠️ 在庫不足・在庫切れの自動検知
- 📱 ChatWorkへの自動通知
- 📊 在庫統計情報の表示
- 🏪 仕入先別の在庫管理

## セットアップ

### 1. 依存関係のインストール

```bash
cd inventory-management
source venv/bin/activate
pip install -r requirements.txt
```

### 2. ChatWork設定

ChatWork通知機能を使用するには、以下の設定が必要です：

1. `.env.example`を`.env`にコピー
2. ChatWork APIトークンを取得
3. 通知を送信するルームIDを確認
4. `.env`ファイルに設定値を記入

```bash
cp .env.example .env
```

`.env`ファイルを編集：
```
CHATWORK_API_TOKEN=your_actual_api_token
CHATWORK_ROOM_ID=your_actual_room_id
```

#### ChatWork APIトークンの取得方法

1. **ChatWorkにログイン**
   - [ChatWork](https://www.chatwork.com/) にアクセス
   - アカウントでログイン

2. **API設定画面にアクセス**
   - 画面右上のプロフィール画像をクリック
   - ドロップダウンメニューから「**サービス連携**」を選択
   - 左側メニューから「**API**」をクリック

3. **APIトークンを作成**
   - 「**新しいトークンを作成**」ボタンをクリック
   - トークン名を入力（例：「在庫管理システム」）
   - 「**作成**」ボタンをクリック
   - 生成されたAPIトークンをコピーして保存

**⚠️ 重要**: APIトークンは一度しか表示されません。必ずコピーして保存してください。

#### ルームIDの確認方法

**方法1: ブラウザのURLから取得（推奨）**
1. ChatWorkにログイン
2. 通知を送信したいルーム（グループチャット）を開く
3. ブラウザのアドレスバーのURLを確認
4. URLの数字部分がルームID

**URL例**: `https://www.chatwork.com/#!rid123456789`
この場合、ルームIDは `123456789` です。

**方法2: API経由で取得**
```bash
curl -X GET \
  -H "X-ChatWorkToken: YOUR_API_TOKEN" \
  "https://api.chatwork.com/v2/rooms"
```

### 3. アプリケーションの起動

```bash
python src/main.py
```

アプリケーションは `http://localhost:5000` で起動します。

## 使用方法

### 初期設定

1. ブラウザで `http://localhost:5000` にアクセス
2. 「📋 初期データを設定」ボタンをクリック
3. サンプル在庫データが設定されます

### 在庫管理

- **在庫減少**: `-0.5` または `-1` ボタンをクリック
- **在庫増加**: `+1` または `+発注数` ボタンをクリック
- **発注通知**: 在庫不足時に表示される「📱 発注通知」ボタンをクリック

### 通知機能

- 在庫が最低値を下回ると自動的にアラートが表示されます
- ChatWork設定が完了している場合、自動的にChatWorkに通知が送信されます
- 手動で発注通知を送信することも可能です

## API エンドポイント

### 在庫管理
- `GET /api/inventory` - 全在庫データ取得
- `POST /api/inventory/{id}/update-stock` - 在庫更新
- `GET /api/inventory/stats` - 統計情報取得
- `POST /api/inventory/initialize` - 初期データ設定

### ChatWork通知
- `POST /api/chatwork/send-notification` - 通知送信
- `POST /api/chatwork/test` - テスト通知送信
- `GET /api/chatwork/config` - 設定状況確認
- `GET /api/chatwork/rooms` - 利用可能ルーム一覧

## トラブルシューティング

### ChatWork通知が送信されない

1. `.env`ファイルの設定を確認
2. APIトークンが正しいか確認
3. ルームIDが正しいか確認
4. `/api/chatwork/test` エンドポイントでテスト送信を試行

### 在庫データが表示されない

1. 「📋 初期データを設定」ボタンをクリック
2. ブラウザの開発者ツールでエラーを確認
3. サーバーログを確認

## 技術仕様

- **バックエンド**: Flask (Python)
- **フロントエンド**: HTML/CSS/JavaScript (Tailwind CSS)
- **データベース**: SQLite
- **通知**: ChatWork API
- **デプロイ**: 任意のPythonホスティング環境



## デプロイ方法

このアプリケーションは複数のプラットフォームにデプロイできます。

### Render.com（推奨）

1. GitHubリポジトリをRender.comに接続
2. 以下の設定を使用：
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `./start.sh`
3. 環境変数を設定：
   - `CHATWORK_API_TOKEN`
   - `CHATWORK_ROOM_ID`
   - `FLASK_ENV=production`

### Heroku

```bash
heroku create your-app-name
heroku config:set CHATWORK_API_TOKEN=your_token
heroku config:set CHATWORK_ROOM_ID=your_room_id
git push heroku main
```

### Vercel

```bash
vercel --prod
```

詳細なデプロイ手順については、プロジェクトに含まれる `flask-deployment-guide.md` を参照してください。

