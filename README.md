# 在庫管理システム

リアルタイム在庫管理とChatWork通知機能を備えた在庫管理Webアプリケーションです。

![在庫管理システム](https://img.shields.io/badge/Status-Active-green)
![License](https://img.shields.io/badge/License-MIT-blue)
![Platform](https://img.shields.io/badge/Platform-Web-orange)

## 🌟 主要機能

### 📦 在庫管理
- **リアルタイム在庫更新**: ボタンクリックで簡単に在庫数を増減
- **カット数対応**: 「○本+カット○」形式での詳細在庫管理
- **多店舗対応**: 複数店舗の在庫を一元管理
- **仕入先別管理**: 6つの仕入先（スジャータ、ライフ、エープライス、ノンヌン、Shein、Amazon）

### 🚨 自動通知機能
- **在庫不足検知**: 最低在庫を下回った際の自動アラート
- **ChatWork通知**: 発注が必要な商品の自動通知
- **テスト通知**: システム動作確認用のテスト機能

### 📊 統計・分析
- **リアルタイム統計**: 総アイテム数、在庫不足数、店舗数、仕入先数
- **高度なフィルタリング**: 店舗、仕入先、カテゴリ、ステータス別表示
- **視覚的ステータス**: 色分けによる在庫状況の直感的把握

### 🎨 ユーザーエクスペリエンス
- **レスポンシブデザイン**: PC・タブレット・スマートフォン対応
- **美しいUI**: グラデーション背景とモダンなデザイン
- **直感的操作**: ワンクリックでの在庫操作

## 🚀 デモ・デプロイ

### ライブデモ
- **Vercel**: [在庫管理システム](https://your-vercel-url.vercel.app) *(デプロイ後に更新)*

### 技術構成
- **フロントエンド**: HTML5, CSS3, JavaScript (ES6+)
- **バックエンド**: Supabase (PostgreSQL)
- **通知**: ChatWork API
- **デプロイ**: Vercel, Render, Heroku対応

## 📋 セットアップ

### 前提条件
- Supabaseアカウント
- ChatWorkアカウント（通知機能を使用する場合）
- Vercel/Render/Herokuアカウント（デプロイする場合）

### 1. リポジトリのクローン
```bash
git clone https://github.com/Tohoso/inventory-management-system.git
cd inventory-management-system
```

### 2. Supabaseプロジェクトの設定

#### データベーステーブルの作成
Supabase SQL Editorで以下のSQLを実行：

```sql
-- 在庫管理テーブルの作成
CREATE TABLE IF NOT EXISTS inventory_items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    current_stock DECIMAL(10,2) NOT NULL DEFAULT 0,
    min_stock DECIMAL(10,2) NOT NULL DEFAULT 1,
    order_qty DECIMAL(10,2) NOT NULL DEFAULT 1,
    unit VARCHAR(20) NOT NULL DEFAULT '個',
    supplier VARCHAR(50) NOT NULL,
    store VARCHAR(50) NOT NULL,
    category VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- RLS設定
ALTER TABLE inventory_items ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all access" ON inventory_items FOR ALL USING (true);
```

#### 初期データの投入
`bulk_insert.sql`ファイルの内容をSupabase SQL Editorで実行して、51件の初期在庫データを投入。

### 3. ChatWork設定

#### APIトークンの取得
1. [ChatWork](https://www.chatwork.com/) にログイン
2. プロフィール画像 → 「サービス連携」
3. 左メニュー「API」→「新しいトークンを作成」
4. トークン名を入力して作成
5. **⚠️ 一度しか表示されないため必ずコピー**

#### ルームIDの確認
- **方法1**: ブラウザのURL確認
  - `https://www.chatwork.com/#!rid123456789` → ルームIDは `123456789`
- **方法2**: API経由で取得
  ```bash
  curl -X GET \
    -H "X-ChatWorkToken: YOUR_TOKEN" \
    "https://api.chatwork.com/v2/rooms"
  ```

## 🌐 デプロイ方法

### Vercel（推奨）

#### 1. Vercelアカウント作成
1. [Vercel](https://vercel.com/) にアクセス
2. 「Sign Up」→「Continue with GitHub」

#### 2. プロジェクトインポート
1. 「New Project」→「Import Git Repository」
2. `inventory-management-system` を選択
3. 「Import」をクリック

#### 3. デプロイ設定
- **Framework Preset**: `Other`
- **Root Directory**: `./`
- **Build Command**: 空白
- **Output Directory**: `web`
- **Install Command**: 空白

#### 4. 環境変数設定
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
CHATWORK_API_TOKEN=your-chatwork-token
CHATWORK_ROOM_ID=your-room-id
```

#### 5. デプロイ実行
「Deploy」ボタンをクリックして1-3分で完了

### その他のプラットフォーム

#### Render.com
```bash
# Build Command
pip install -r requirements.txt

# Start Command
./start.sh
```

#### Heroku
```bash
heroku create your-app-name
heroku config:set CHATWORK_API_TOKEN=your_token
heroku config:set CHATWORK_ROOM_ID=your_room_id
git push heroku main
```

詳細な手順は `vercel-deployment-guide.md` を参照。

## 📱 使用方法

### 基本操作
1. **データ更新**: 「🔄 データ更新」ボタンで最新データを取得
2. **在庫調整**: 各アイテムの +/- ボタンで在庫を増減
3. **発注通知**: 在庫不足時に「📱 発注通知」でChatWorkに通知
4. **フィルタリング**: 上部のフィルターで表示を絞り込み

### カット数管理
- **対象アイテム**: チーズケーキ、ブラウニーなど
- **表示形式**: 「○本+カット○」
- **操作**: 本数・カット数を個別に調整可能
- **更新**: 入力フィールドで直接編集 → 「更新」ボタン

### 通知機能
- **自動検知**: 在庫が最低値を下回ると自動アラート
- **手動通知**: 「📱 発注通知」ボタンで即座に通知
- **テスト機能**: 「🧪 ChatWorkテスト」で動作確認

## 🔧 API仕様

### 在庫管理エンドポイント
- `GET /rest/v1/inventory_items` - 全在庫データ取得
- `PATCH /rest/v1/inventory_items?id=eq.{id}` - 在庫更新

### ChatWork通知
- `POST /v2/rooms/{room_id}/messages` - メッセージ送信

## 📊 対応データ

### 店舗
- **Melt**: 21アイテム
- **ノンヌン**: 30アイテム

### 仕入先
- **スジャータ**: 乳製品・アイス類
- **ライフ**: 飲料・食材・調味料
- **エープライス**: 製菓材料・ソース類
- **ノンヌン**: ケーキ・デザート類
- **Shein**: 装飾品・ストロー類
- **Amazon**: クッキー・トッピング類

### カテゴリ
- 乳製品、アイス、飲料、調味料、製菓材料、食材、ソース、装飾品、果物

## 🛠️ トラブルシューティング

### よくある問題

#### データが表示されない
1. ブラウザの開発者ツール（F12）でエラーを確認
2. Supabase接続設定を確認
3. 「🔄 データ更新」ボタンを再クリック

#### ChatWork通知が送信されない
1. APIトークンの有効性を確認
2. ルームIDが正しいか確認
3. ルームに参加しているか確認
4. 「🧪 ChatWorkテスト」で動作確認

#### デプロイエラー
1. 環境変数の設定を確認
2. `vercel.json`の設定を確認
3. ビルドログでエラー詳細を確認

### サポート
- **Issues**: [GitHub Issues](https://github.com/Tohoso/inventory-management-system/issues)
- **Documentation**: プロジェクト内の各種ガイドファイル

## 📄 ライセンス

MIT License - 詳細は [LICENSE](LICENSE) ファイルを参照

## 🤝 コントリビューション

1. このリポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📞 サポート・お問い合わせ

- **GitHub Issues**: バグ報告・機能要望
- **Email**: [お問い合わせ先メールアドレス]
- **ChatWork**: システム管理者まで

---

**在庫管理システム** - 効率的な在庫管理でビジネスをサポート 🚀

