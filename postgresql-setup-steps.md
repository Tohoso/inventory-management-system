# PostgreSQL設定 - 具体的手順

## 🎯 今すぐ実行する手順

### ステップ1: Renderでデータベース作成

1. **Renderダッシュボードにアクセス**
   - https://dashboard.render.com/ にログイン

2. **PostgreSQLデータベースを作成**
   - 「**New +**」ボタンをクリック
   - 「**PostgreSQL**」を選択

3. **設定項目を入力**
   ```
   Name: inventory-management-db
   Database: inventory_db
   User: inventory_user
   Region: Singapore (Asia) ← 日本から近い
   Plan: Basic-256mb ($6/月) ← 本格運用の場合
   ```

4. **「Create Database」をクリック**
   - 数分でデータベースが作成されます

### ステップ2: 接続情報をコピー

データベース作成後、「Info」タブで以下をコピー：

```
Internal Database URL: postgresql://user:password@hostname:port/database
```

**この URL をコピーしてください！**

### ステップ3: Webサービスに環境変数を設定

1. **Webサービスの管理画面にアクセス**
   - あなたの在庫管理アプリのページを開く

2. **「Environment」タブをクリック**

3. **環境変数を追加**
   ```
   Key: DATABASE_URL
   Value: [ステップ2でコピーしたURL]
   ```

4. **他の環境変数も設定**
   ```
   FLASK_ENV=production
   CHATWORK_API_TOKEN=your_actual_token
   CHATWORK_ROOM_ID=your_actual_room_id
   SECRET_KEY=your_secret_key
   ```

### ステップ4: コードの更新（完了済み）

✅ 既に以下の修正を実施済み：
- `requirements.txt` に `psycopg2-binary==2.9.7` を追加
- `main.py` でPostgreSQL対応のデータベース設定に更新

### ステップ5: GitHubにプッシュ

```bash
git add .
git commit -m "Add PostgreSQL support for production deployment"
git push origin main
```

### ステップ6: デプロイ確認

1. **Renderで自動デプロイが開始**
   - GitHubプッシュ後、数分で再デプロイが完了

2. **アプリケーションにアクセス**
   - デプロイされたURLを開く

3. **データベース接続確認**
   - 「📋 初期データを設定」をクリック
   - データが正常に保存されることを確認

## 💰 料金について

### 推奨プラン
- **Webサービス**: Free (750時間/月) または Starter ($7/月)
- **PostgreSQL**: Basic-256mb ($6/月)
- **合計**: $6/月 または $13/月

### 無料で試したい場合
- **PostgreSQL**: Free (90日間制限)
- **合計**: $0 (90日間のみ)

## 🔍 設定確認方法

### データベース接続確認
```bash
# アプリのログを確認
curl -X GET https://your-app-url.onrender.com/api/inventory/items
```

### 環境変数確認
Renderの管理画面「Environment」タブで設定値を確認

## 🚨 トラブルシューティング

### よくあるエラー

1. **接続エラー**
   - DATABASE_URLが正しく設定されているか確認
   - Internal Database URLを使用しているか確認

2. **デプロイエラー**
   - requirements.txtにpsycopg2-binaryが含まれているか確認
   - GitHubに最新コードがプッシュされているか確認

3. **データが保存されない**
   - 環境変数DATABASE_URLが設定されているか確認
   - PostgreSQLデータベースが正常に作成されているか確認

## ✅ 完了チェックリスト

- [ ] RenderでPostgreSQLデータベースを作成
- [ ] Internal Database URLをコピー
- [ ] WebサービスにDATABASE_URL環境変数を設定
- [ ] 他の環境変数（FLASK_ENV, CHATWORK_*）を設定
- [ ] GitHubに最新コードをプッシュ
- [ ] Renderで再デプロイ完了
- [ ] アプリケーションにアクセスして動作確認
- [ ] 初期データ設定が正常に動作することを確認

この手順に従えば、PostgreSQLを使用した本格的な在庫管理システムが完成します！

