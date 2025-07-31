# Vercel デプロイメントガイド

## 🚀 Vercelでの在庫管理システムデプロイ手順

### **前提条件**
- GitHubアカウント
- Vercelアカウント（GitHubでサインアップ可能）

### **手順1: Vercelアカウント作成**

1. **[Vercel](https://vercel.com/)** にアクセス
2. **「Sign Up」**をクリック
3. **「Continue with GitHub」**を選択
4. GitHubアカウントでログイン
5. 必要な権限を許可

### **手順2: プロジェクトのインポート**

1. **Vercelダッシュボード**で「New Project」をクリック
2. **「Import Git Repository」**を選択
3. **リポジトリを検索**: `inventory-management-system`
4. **「Import」**をクリック

### **手順3: デプロイ設定**

#### **基本設定**
- **Project Name**: `inventory-management-system`
- **Framework Preset**: `Other`
- **Root Directory**: `./` (デフォルト)

#### **Build Settings**
- **Build Command**: 空白のまま（静的サイト）
- **Output Directory**: `web`
- **Install Command**: 空白のまま

#### **Environment Variables（環境変数）**
以下の環境変数を設定：

```env
SUPABASE_URL=https://yyoixwdljeoxtieeazfo.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl5b2l4d2RsamVveHRpZWVhemZvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM5MjY3NTQsImV4cCI6MjA2OTUwMjc1NH0.Lp1GLRlXI57odcpNhSl5TB2bOKSSW5Ce66_KuO_7tFs
CHATWORK_API_TOKEN=5f149c4cd0bf7044e532b70d574ba655
CHATWORK_ROOM_ID=405830596
```

### **手順4: デプロイ実行**

1. **「Deploy」**ボタンをクリック
2. **ビルド完了を待機**（通常1-3分）
3. **デプロイ完了後、URLが発行される**

### **手順5: カスタムドメイン設定（オプション）**

1. **プロジェクト設定**で「Domains」タブ
2. **「Add Domain」**をクリック
3. **独自ドメインを入力**（例: `inventory.yourdomain.com`）
4. **DNS設定を更新**

## 🔧 Vercel設定ファイル

### **vercel.json**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "web/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/web/$1"
    },
    {
      "src": "/",
      "dest": "/web/index.html"
    }
  ]
}
```

## 🌟 Vercelの利点

### **パフォーマンス**
- **グローバルCDN**: 世界中で高速アクセス
- **自動最適化**: 画像・CSS・JSの自動最適化
- **HTTP/2対応**: 高速通信プロトコル

### **開発体験**
- **自動デプロイ**: GitHubプッシュで自動更新
- **プレビューURL**: プルリクエストごとにプレビュー
- **ロールバック**: ワンクリックで前バージョンに戻す

### **セキュリティ**
- **HTTPS自動対応**: SSL証明書の自動発行・更新
- **DDoS保護**: 自動的な攻撃防御
- **セキュリティヘッダー**: 自動的なセキュリティ強化

### **監視・分析**
- **リアルタイム分析**: アクセス状況の詳細分析
- **パフォーマンス監視**: ページ読み込み速度の監視
- **エラー追跡**: 自動的なエラー検出・通知

## 📊 料金プラン

### **Hobby（無料）**
- **帯域幅**: 100GB/月
- **ビルド時間**: 6,000分/月
- **プロジェクト数**: 無制限
- **カスタムドメイン**: 対応

### **Pro（$20/月）**
- **帯域幅**: 1TB/月
- **ビルド時間**: 24,000分/月
- **チーム機能**: 対応
- **優先サポート**: 対応

## 🔄 継続的デプロイ

### **自動デプロイ設定**
1. **GitHubリポジトリ更新**
2. **Vercelが自動検知**
3. **自動ビルド・デプロイ**
4. **新しいURLで即座にアクセス可能**

### **ブランチデプロイ**
- **main**: 本番環境
- **develop**: ステージング環境
- **feature/***: プレビュー環境

## 🛠️ トラブルシューティング

### **よくある問題**

#### **ビルドエラー**
```bash
# 解決方法
1. vercel.jsonの設定確認
2. ファイルパスの確認
3. 環境変数の設定確認
```

#### **404エラー**
```bash
# 解決方法
1. Output Directoryの設定確認
2. ルーティング設定の確認
3. ファイル名の大文字小文字確認
```

#### **API接続エラー**
```bash
# 解決方法
1. 環境変数の設定確認
2. CORS設定の確認
3. APIキーの有効性確認
```

## 📞 サポート

### **公式ドキュメント**
- [Vercel Documentation](https://vercel.com/docs)
- [Deployment Guide](https://vercel.com/docs/concepts/deployments/overview)

### **コミュニティ**
- [Vercel Discord](https://vercel.com/discord)
- [GitHub Discussions](https://github.com/vercel/vercel/discussions)

---

**このガイドに従って、在庫管理システムをVercelで簡単にデプロイできます！**

