# ChatWork 500エラー デバッグガイド

## 🚨 発生している問題

**エラー**: `HTTP error! status: 500`
**場所**: ChatWork通知送信時
**原因**: サーバーサイドエラー（環境変数設定の問題の可能性）

## 🔍 考えられる原因

### 1. 環境変数が設定されていない
- `CHATWORK_API_TOKEN` が未設定
- `CHATWORK_ROOM_ID` が未設定

### 2. ChatWork APIトークンが無効
- トークンが間違っている
- トークンの有効期限が切れている

### 3. ルームIDが間違っている
- 存在しないルームID
- アクセス権限がないルーム

## 🛠️ 修正内容

### 1. 詳細なログ出力を追加
- リクエストデータの詳細ログ
- ChatWork設定状況の確認
- API レスポンスの詳細ログ
- エラー時のデバッグ情報

### 2. エラーハンドリングの改善
- より具体的なエラーメッセージ
- デバッグ情報の追加
- 設定状況の詳細表示

## 🔧 確認手順

### ステップ1: 環境変数の確認

Renderの管理画面で以下の環境変数が正しく設定されているか確認：

```env
CHATWORK_API_TOKEN=your_actual_token_here
CHATWORK_ROOM_ID=your_actual_room_id_here
FLASK_ENV=production
```

### ステップ2: 設定状況の確認

アプリケーションで以下のURLにアクセス：
```
https://your-app-url.onrender.com/api/chatwork/config
```

正常な場合のレスポンス例：
```json
{
  "success": true,
  "config": {
    "api_token_set": true,
    "room_id_set": true,
    "api_token_length": 40,
    "room_id": "123456789"
  }
}
```

### ステップ3: テスト通知の送信

以下のURLでテスト通知を送信：
```
https://your-app-url.onrender.com/api/chatwork/test
```

### ステップ4: ログの確認

Renderの管理画面でアプリケーションログを確認し、詳細なエラー情報を取得。

## 🎯 解決策

### 解決策1: 環境変数の再設定

1. **Renderの管理画面にアクセス**
2. **「Environment」タブを開く**
3. **以下の環境変数を確認・設定**：
   ```
   CHATWORK_API_TOKEN: [あなたのAPIトークン]
   CHATWORK_ROOM_ID: [あなたのルームID]
   ```
4. **「Save Changes」をクリック**
5. **アプリケーションが自動再デプロイされるのを待つ**

### 解決策2: ChatWork APIトークンの再作成

1. **ChatWorkにログイン**
2. **プロフィール → サービス連携 → API**
3. **新しいトークンを作成**
4. **新しいトークンをRenderの環境変数に設定**

### 解決策3: ルームIDの再確認

1. **ChatWorkで通知を送信したいルームを開く**
2. **URLから数字部分を確認**
   ```
   https://www.chatwork.com/#!rid123456789
   → ルームID: 123456789
   ```
3. **正しいルームIDをRenderの環境変数に設定**

## 📝 修正後の確認方法

### 1. 設定確認API
```bash
curl https://your-app-url.onrender.com/api/chatwork/config
```

### 2. テスト通知API
```bash
curl -X POST https://your-app-url.onrender.com/api/chatwork/test
```

### 3. 実際の通知テスト
1. アプリケーションで在庫を最低値以下にする
2. 「📱 発注通知」ボタンをクリック
3. ChatWorkに通知が送信されることを確認

## 🚀 次のステップ

1. **修正されたコードをGitHubにプッシュ**
2. **Renderで自動再デプロイ**
3. **環境変数の設定確認**
4. **テスト通知の送信**
5. **実際の通知機能の確認**

この修正により、500エラーの詳細な原因が特定でき、適切な解決策を実行できるようになります。

