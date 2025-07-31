# Supabase Edge Functions デプロイガイド

## 🚀 Edge Functions 手動デプロイ手順

### ステップ1: 在庫管理API Function作成

1. **[Supabase Dashboard](https://supabase.com/dashboard)** にアクセス
2. **プロジェクト「yyoixwdljeoxtieeazfo」**を選択
3. **左メニュー「Edge Functions」**をクリック
4. **「Create a new function」**をクリック
5. **Function名**: `inventory-api`
6. **以下のコードをコピー&ペースト**：

```typescript
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
    )

    const url = new URL(req.url)
    const path = url.pathname

    console.log(`Request: ${req.method} ${path}`)

    if (req.method === 'GET' && path === '/inventory') {
      const { data, error } = await supabase
        .from('inventory_items')
        .select('*')
        .order('store', { ascending: true })
        .order('supplier', { ascending: true })
        .order('name', { ascending: true })

      if (error) throw error

      return new Response(
        JSON.stringify({ success: true, data }),
        { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      )
    }

    if (req.method === 'PUT' && path.startsWith('/inventory/')) {
      const id = path.split('/')[2]
      const requestData = await req.json()
      const { current_stock } = requestData

      const { data, error } = await supabase
        .from('inventory_items')
        .update({ current_stock })
        .eq('id', id)
        .select()
        .single()

      if (error) throw error

      return new Response(
        JSON.stringify({ success: true, data }),
        { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      )
    }

    if (req.method === 'GET' && path.startsWith('/inventory/')) {
      const id = path.split('/')[2]
      const { data, error } = await supabase
        .from('inventory_items')
        .select('*')
        .eq('id', id)
        .single()

      if (error) throw error

      return new Response(
        JSON.stringify({ success: true, data }),
        { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      )
    }

    if (req.method === 'GET' && path === '/stats') {
      const { data, error } = await supabase
        .from('inventory_items')
        .select('store, supplier, category, current_stock, min_stock')

      if (error) throw error

      const totalItems = data?.length || 0
      const lowStockItems = data?.filter(item => item.current_stock <= item.min_stock).length || 0
      const stores = [...new Set(data?.map(item => item.store) || [])]
      const suppliers = [...new Set(data?.map(item => item.supplier) || [])]

      const stats = {
        totalItems,
        lowStockItems,
        stores: stores.length,
        suppliers: suppliers.length
      }

      return new Response(
        JSON.stringify({ success: true, data: stats }),
        { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      )
    }

    return new Response(
      JSON.stringify({ error: 'Not Found' }),
      { status: 404, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )

  } catch (error) {
    console.error('Function error:', error)
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )
  }
})
```

7. **「Deploy function」**をクリック

### ステップ2: ChatWork API Function作成

1. **「Create a new function」**をクリック
2. **Function名**: `chatwork-api`
3. **以下のコードをコピー&ペースト**：

```typescript
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const url = new URL(req.url)
    const path = url.pathname

    if (req.method === 'POST' && path === '/send-notification') {
      const data = await req.json()
      
      const CHATWORK_API_TOKEN = Deno.env.get('CHATWORK_API_TOKEN')
      const CHATWORK_ROOM_ID = Deno.env.get('CHATWORK_ROOM_ID')

      if (!CHATWORK_API_TOKEN || !CHATWORK_ROOM_ID) {
        return new Response(
          JSON.stringify({ 
            success: false, 
            error: 'ChatWork設定が不完全です' 
          }),
          { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
        )
      }

      const message = `
🚨 在庫アラート

商品名: ${data.item_name}
現在の在庫: ${data.current_stock}${data.unit}
最低在庫: ${data.min_stock}${data.unit}
推奨発注数: ${data.order_qty}${data.unit}
仕入先: ${data.supplier}
店舗: ${data.store || ''}

発注をお願いします。
通知時刻: ${new Date().toLocaleString('ja-JP', { timeZone: 'Asia/Tokyo' })}
      `.trim()

      const response = await fetch(
        `https://api.chatwork.com/v2/rooms/${CHATWORK_ROOM_ID}/messages`,
        {
          method: 'POST',
          headers: {
            'X-ChatWorkToken': CHATWORK_API_TOKEN,
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          body: new URLSearchParams({ body: message })
        }
      )

      if (response.ok) {
        const chatworkResponse = await response.json()
        return new Response(
          JSON.stringify({ 
            success: true, 
            message: 'ChatWork通知を送信しました',
            chatwork_response: chatworkResponse
          }),
          { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
        )
      } else {
        const errorText = await response.text()
        return new Response(
          JSON.stringify({ 
            success: false, 
            error: `ChatWork API エラー: ${response.status}`,
            details: errorText
          }),
          { status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
        )
      }
    }

    if (req.method === 'POST' && path === '/test') {
      const CHATWORK_API_TOKEN = Deno.env.get('CHATWORK_API_TOKEN')
      const CHATWORK_ROOM_ID = Deno.env.get('CHATWORK_ROOM_ID')

      if (!CHATWORK_API_TOKEN || !CHATWORK_ROOM_ID) {
        return new Response(
          JSON.stringify({ 
            success: false, 
            error: 'ChatWork設定が不完全です' 
          }),
          { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
        )
      }

      const testMessage = `
🧪 在庫管理システム テスト通知

このメッセージは在庫管理システムからのテスト通知です。
システムが正常に動作していることを確認しました。

送信時刻: ${new Date().toLocaleString('ja-JP', { timeZone: 'Asia/Tokyo' })}
      `.trim()

      const response = await fetch(
        `https://api.chatwork.com/v2/rooms/${CHATWORK_ROOM_ID}/messages`,
        {
          method: 'POST',
          headers: {
            'X-ChatWorkToken': CHATWORK_API_TOKEN,
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          body: new URLSearchParams({ body: testMessage })
        }
      )

      if (response.ok) {
        const chatworkResponse = await response.json()
        return new Response(
          JSON.stringify({ 
            success: true, 
            message: 'テスト通知を送信しました',
            chatwork_response: chatworkResponse
          }),
          { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
        )
      } else {
        const errorText = await response.text()
        return new Response(
          JSON.stringify({ 
            success: false, 
            error: `ChatWork API エラー: ${response.status}`,
            details: errorText
          }),
          { status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
        )
      }
    }

    return new Response(
      JSON.stringify({ error: 'Not Found' }),
      { status: 404, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )

  } catch (error) {
    console.error('ChatWork API function error:', error)
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )
  }
})
```

4. **「Deploy function」**をクリック

### ステップ3: 環境変数設定

1. **左メニュー「Settings」→「Edge Functions」**をクリック
2. **「Environment variables」**セクション
3. **以下の環境変数を追加**：

```
CHATWORK_API_TOKEN = 5f149c4cd0bf7044e532b70d574ba655
CHATWORK_ROOM_ID = 405830596
```

4. **「Save」**をクリック

### ステップ4: デプロイ確認

両方のFunctionがデプロイされると、以下のURLでアクセス可能になります：

- **在庫API**: `https://yyoixwdljeoxtieeazfo.supabase.co/functions/v1/inventory-api`
- **ChatWork API**: `https://yyoixwdljeoxtieeazfo.supabase.co/functions/v1/chatwork-api`

## 🎯 次のステップ

Edge Functionsのデプロイが完了したら、フロントエンドの設定を行います。

