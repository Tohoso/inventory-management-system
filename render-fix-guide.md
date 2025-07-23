# Render デプロイ修正ガイド

## 🚨 発生していた問題

**エラー**: `sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) unable to open database file`

**原因**: Renderのような本番環境では、ファイルシステムが読み取り専用のため、SQLiteファイルの作成・書き込みができない。

## ✅ 実装した解決策

### 1. データベース設定の変更

`src/main.py` のデータベース設定を環境に応じて切り替えるように修正：

```python
# データベース設定 - 本番環境対応
if os.environ.get('FLASK_ENV') == 'production':
    # 本番環境ではインメモリSQLiteを使用
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
else:
    # 開発環境では通常のファイルベースSQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
```

### 2. 環境変数の設定

Renderの環境変数に以下を設定：
- `FLASK_ENV=production`

## 🔄 インメモリデータベースの特徴

### メリット
- ✅ ファイルシステムの制限を回避
- ✅ 高速なデータアクセス
- ✅ デプロイが簡単

### 注意点
- ⚠️ アプリケーション再起動時にデータが消失
- ⚠️ 複数インスタンス間でのデータ共有不可

## 🚀 Render での正しいデプロイ手順

### 1. 環境変数の設定

Renderの管理画面で以下の環境変数を設定：

```env
FLASK_ENV=production
CHATWORK_API_TOKEN=your_actual_token
CHATWORK_ROOM_ID=your_actual_room_id
SECRET_KEY=your_secret_key
```

### 2. ビルド設定

- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `./start.sh`

### 3. 初期データの設定

アプリケーション起動後、以下の手順で初期データを設定：

1. デプロイされたURLにアクセス
2. 「📋 初期データを設定」ボタンをクリック
3. サンプル在庫データが設定される

**注意**: アプリケーション再起動のたびに初期データの設定が必要です。

## 🔧 代替案（永続化が必要な場合）

### PostgreSQL を使用する場合

#### 1. Render PostgreSQL データベースの作成

1. Renderダッシュボードで「New」→「PostgreSQL」
2. データベース名を設定
3. 作成されたDATABASE_URLをコピー

#### 2. requirements.txt の更新

```txt
psycopg2-binary==2.9.7
```

#### 3. main.py の修正

```python
import os

# データベース設定
database_url = os.environ.get('DATABASE_URL')
if database_url:
    # PostgreSQL使用（本番環境）
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
elif os.environ.get('FLASK_ENV') == 'production':
    # インメモリSQLite（本番環境でPostgreSQLが設定されていない場合）
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
else:
    # ファイルベースSQLite（開発環境）
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
```

#### 4. 環境変数の追加

```env
DATABASE_URL=postgresql://username:password@hostname:port/database_name
```

## 📝 今回の修正内容まとめ

1. **環境に応じたデータベース設定**: 本番環境ではインメモリSQLiteを使用
2. **ファイルシステム制限の回避**: 読み取り専用環境でも動作
3. **簡単なデプロイ**: 追加の設定なしでRenderにデプロイ可能

## 🎯 次のステップ

1. 修正されたコードをGitHubにプッシュ
2. Renderで再デプロイ
3. 環境変数 `FLASK_ENV=production` を設定
4. アプリケーションの動作確認
5. 初期データの設定

この修正により、Renderでのデプロイが正常に動作するはずです。

