// Vercel Edge Function for ChatWork API proxy
export default async function handler(req, res) {
    // CORS設定
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

    // OPTIONSリクエスト（プリフライト）への対応
    if (req.method === 'OPTIONS') {
        res.status(200).end();
        return;
    }

    // POSTリクエストのみ許可
    if (req.method !== 'POST') {
        res.status(405).json({ error: 'Method not allowed' });
        return;
    }

    try {
        // Vercel環境変数から設定を取得
        const CHATWORK_API_TOKEN = process.env.CHATWORK_API_TOKEN;
        const CHATWORK_ROOM_ID = process.env.CHATWORK_ROOM_ID;

        // 環境変数の確認
        if (!CHATWORK_API_TOKEN || !CHATWORK_ROOM_ID) {
            console.error('Missing environment variables:', {
                hasToken: !!CHATWORK_API_TOKEN,
                hasRoomId: !!CHATWORK_ROOM_ID
            });
            res.status(500).json({ 
                error: 'Server configuration error: Missing ChatWork credentials' 
            });
            return;
        }

        const { message } = req.body;

        // 必須パラメータの確認
        if (!message) {
            res.status(400).json({ 
                error: 'Missing required parameter: message' 
            });
            return;
        }

        console.log('Sending ChatWork message to room:', CHATWORK_ROOM_ID);

        // ChatWork APIへのリクエスト
        const chatworkResponse = await fetch(`https://api.chatwork.com/v2/rooms/${CHATWORK_ROOM_ID}/messages`, {
            method: 'POST',
            headers: {
                'X-ChatWorkToken': CHATWORK_API_TOKEN,
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                body: message
            })
        });

        if (chatworkResponse.ok) {
            const result = await chatworkResponse.json();
            console.log('ChatWork API Success:', result);
            res.status(200).json({
                success: true,
                message: 'ChatWork notification sent successfully',
                data: result
            });
        } else {
            const errorText = await chatworkResponse.text();
            console.error('ChatWork API Error:', chatworkResponse.status, errorText);
            res.status(chatworkResponse.status).json({
                success: false,
                error: `ChatWork API Error: ${chatworkResponse.status}`,
                details: errorText
            });
        }

    } catch (error) {
        console.error('Server Error:', error);
        res.status(500).json({
            success: false,
            error: 'Internal server error',
            details: error.message
        });
    }
}

