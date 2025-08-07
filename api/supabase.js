export default async function handler(req, res) {
  // CORS設定
  res.setHeader('Access-Control-Allow-Origin', '*')
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization')

  // OPTIONSリクエストの処理
  if (req.method === 'OPTIONS') {
    res.status(200).end()
    return
  }

  try {
    console.log('=== Supabase Proxy API Debug Start ===')
    console.log('Request method:', req.method)
    console.log('Request query:', req.query)
    console.log('Request body:', req.body)

    // 環境変数の確認
    const SUPABASE_URL = process.env.SUPABASE_URL || 'https://yyoixwdljeoxtieeazfo.supabase.co'
    const SUPABASE_ANON_KEY = process.env.SUPABASE_ANON_KEY

    console.log('Environment check:', {
      hasSupabaseUrl: !!SUPABASE_URL,
      hasSupabaseKey: !!SUPABASE_ANON_KEY,
      supabaseUrl: SUPABASE_URL,
      keyLength: SUPABASE_ANON_KEY?.length || 0
    })

    if (!SUPABASE_ANON_KEY) {
      console.error('Missing SUPABASE_ANON_KEY environment variable')
      return res.status(500).json({ 
        error: 'Server configuration error',
        details: 'Missing SUPABASE_ANON_KEY environment variable'
      })
    }

    // エンドポイントの取得
    const endpoint = req.query.endpoint
    if (!endpoint) {
      console.error('Missing endpoint parameter')
      return res.status(400).json({ 
        error: 'Bad request',
        details: 'Missing endpoint parameter'
      })
    }

    // Supabase APIのURL構築
    const supabaseApiUrl = `${SUPABASE_URL}/rest/v1/${endpoint}`
    console.log('Supabase API URL:', supabaseApiUrl)

    // リクエストヘッダーの設定
    const headers = {
      'apikey': SUPABASE_ANON_KEY,
      'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
      'Content-Type': 'application/json',
      'Prefer': 'return=minimal'
    }

    // リクエストオプションの設定
    const fetchOptions = {
      method: req.method,
      headers: headers
    }

    // POSTやPATCHの場合はボディを追加
    if (req.method === 'POST' || req.method === 'PATCH' || req.method === 'PUT') {
      fetchOptions.body = JSON.stringify(req.body)
    }

    console.log('Fetch options:', {
      method: fetchOptions.method,
      url: supabaseApiUrl,
      hasBody: !!fetchOptions.body
    })

    // Supabase APIへのリクエスト
    const response = await fetch(supabaseApiUrl, fetchOptions)
    console.log('Supabase API response status:', response.status)

    if (!response.ok) {
      const errorText = await response.text()
      console.error('Supabase API error:', {
        status: response.status,
        statusText: response.statusText,
        errorText: errorText
      })
      
      return res.status(response.status).json({
        error: 'Supabase API error',
        status: response.status,
        details: errorText
      })
    }

    // レスポンスの処理
    const contentType = response.headers.get('content-type')
    let data

    if (contentType && contentType.includes('application/json')) {
      data = await response.json()
    } else {
      data = await response.text()
    }

    console.log('Supabase API response data:', data)
    console.log('=== Supabase Proxy API Debug End ===')

    // 成功レスポンス
    res.status(200).json(data)

  } catch (error) {
    console.error('Supabase Proxy API error details:', {
      message: error.message,
      stack: error.stack
    })

    res.status(500).json({
      error: 'Internal server error',
      details: error.message
    })
  }
}

