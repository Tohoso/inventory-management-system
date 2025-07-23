from flask import Blueprint, request, jsonify
import requests
import os
from datetime import datetime
import logging

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

chatwork_bp = Blueprint('chatwork', __name__)

# ChatWork設定（環境変数から取得）
CHATWORK_API_TOKEN = os.getenv('CHATWORK_API_TOKEN', '')
CHATWORK_ROOM_ID = os.getenv('CHATWORK_ROOM_ID', '')
CHATWORK_API_BASE = 'https://api.chatwork.com/v2'

@chatwork_bp.route('/chatwork/send-notification', methods=['POST'])
def send_notification():
    """在庫アラート通知をChatWorkに送信"""
    try:
        logger.info("ChatWork通知リクエストを受信")
        
        data = request.get_json()
        if not data:
            logger.error("リクエストデータが空です")
            return jsonify({
                'success': False,
                'error': 'データが提供されていません'
            }), 400
        
        logger.info(f"受信データ: {data}")
        
        # 必要なパラメータをチェック
        required_fields = ['item_name', 'current_stock', 'min_stock', 'unit']
        for field in required_fields:
            if field not in data:
                logger.error(f"必須フィールド {field} が不足")
                return jsonify({
                    'success': False,
                    'error': f'必須フィールド {field} が不足しています'
                }), 400
        
        # ChatWork設定をチェック
        logger.info(f"ChatWork設定確認 - API_TOKEN: {'設定済み' if CHATWORK_API_TOKEN else '未設定'}, ROOM_ID: {CHATWORK_ROOM_ID}")
        
        if not CHATWORK_API_TOKEN or not CHATWORK_ROOM_ID:
            logger.error("ChatWork設定が不完全")
            return jsonify({
                'success': False,
                'error': 'ChatWork設定が不完全です。API_TOKENとROOM_IDを設定してください。',
                'config_needed': True,
                'debug_info': {
                    'api_token_set': bool(CHATWORK_API_TOKEN),
                    'room_id_set': bool(CHATWORK_ROOM_ID),
                    'api_token_length': len(CHATWORK_API_TOKEN) if CHATWORK_API_TOKEN else 0
                }
            }), 400
        
        # 通知メッセージを作成
        item_name = data['item_name']
        current_stock = data['current_stock']
        min_stock = data['min_stock']
        unit = data['unit']
        order_qty = data.get('order_qty', 1)
        supplier = data.get('supplier', '未設定')
        
        # 在庫状況を判定
        if current_stock <= 0:
            status_icon = '🚨'
            status_text = '在庫切れ'
            urgency = '[緊急]'
        else:
            status_icon = '⚠️'
            status_text = '在庫不足'
            urgency = '[要注意]'
        
        message = f"""
{urgency} {status_icon} 在庫アラート

商品名: {item_name}
現在の在庫: {current_stock}{unit}
最低在庫: {min_stock}{unit}
状況: {status_text}
推奨発注数: {order_qty}{unit}
仕入先: {supplier}

発注をお願いします。
通知時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """.strip()
        
        logger.info(f"送信メッセージ: {message}")
        
        # ChatWork APIに送信
        headers = {
            'X-ChatWorkToken': CHATWORK_API_TOKEN,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        payload = {
            'body': message
        }
        
        api_url = f'{CHATWORK_API_BASE}/rooms/{CHATWORK_ROOM_ID}/messages'
        logger.info(f"ChatWork API URL: {api_url}")
        
        response = requests.post(
            api_url,
            headers=headers,
            data=payload,
            timeout=10
        )
        
        logger.info(f"ChatWork API レスポンス: ステータス={response.status_code}, 内容={response.text}")
        
        if response.status_code == 200:
            logger.info("ChatWork通知送信成功")
            return jsonify({
                'success': True,
                'message': 'ChatWork通知を送信しました',
                'chatwork_response': response.json()
            })
        else:
            logger.error(f"ChatWork API エラー: {response.status_code} - {response.text}")
            return jsonify({
                'success': False,
                'error': f'ChatWork API エラー: {response.status_code}',
                'details': response.text,
                'debug_info': {
                    'api_url': api_url,
                    'room_id': CHATWORK_ROOM_ID,
                    'api_token_length': len(CHATWORK_API_TOKEN)
                }
            }), 500
            
    except requests.exceptions.RequestException as e:
        logger.error(f"ChatWork API接続エラー: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'ChatWork API接続エラー: {str(e)}'
        }), 500
    except Exception as e:
        logger.error(f"予期しないエラー: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'予期しないエラー: {str(e)}'
        }), 500

@chatwork_bp.route('/chatwork/test', methods=['POST'])
def test_notification():
    """ChatWork通知のテスト送信"""
    try:
        # ChatWork設定をチェック
        if not CHATWORK_API_TOKEN or not CHATWORK_ROOM_ID:
            return jsonify({
                'success': False,
                'error': 'ChatWork設定が不完全です。API_TOKENとROOM_IDを設定してください。',
                'config_needed': True
            }), 400
        
        # テストメッセージを作成
        message = f"""
🧪 在庫管理システム テスト通知

このメッセージは在庫管理システムからのテスト通知です。
システムが正常に動作していることを確認しました。

送信時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """.strip()
        
        # ChatWork APIに送信
        headers = {
            'X-ChatWorkToken': CHATWORK_API_TOKEN,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        payload = {
            'body': message
        }
        
        response = requests.post(
            f'{CHATWORK_API_BASE}/rooms/{CHATWORK_ROOM_ID}/messages',
            headers=headers,
            data=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            return jsonify({
                'success': True,
                'message': 'テスト通知を送信しました',
                'chatwork_response': response.json()
            })
        else:
            return jsonify({
                'success': False,
                'error': f'ChatWork API エラー: {response.status_code}',
                'details': response.text
            }), 500
            
    except requests.exceptions.RequestException as e:
        return jsonify({
            'success': False,
            'error': f'ChatWork API接続エラー: {str(e)}'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'予期しないエラー: {str(e)}'
        }), 500

@chatwork_bp.route('/chatwork/config', methods=['GET'])
def get_config():
    """ChatWork設定状況を確認"""
    return jsonify({
        'success': True,
        'config': {
            'api_token_set': bool(CHATWORK_API_TOKEN),
            'room_id_set': bool(CHATWORK_ROOM_ID),
            'api_token_length': len(CHATWORK_API_TOKEN) if CHATWORK_API_TOKEN else 0,
            'room_id': CHATWORK_ROOM_ID if CHATWORK_ROOM_ID else None
        }
    })

@chatwork_bp.route('/chatwork/rooms', methods=['GET'])
def get_rooms():
    """利用可能なChatWorkルーム一覧を取得"""
    try:
        if not CHATWORK_API_TOKEN:
            return jsonify({
                'success': False,
                'error': 'ChatWork API_TOKENが設定されていません'
            }), 400
        
        headers = {
            'X-ChatWorkToken': CHATWORK_API_TOKEN
        }
        
        response = requests.get(
            f'{CHATWORK_API_BASE}/rooms',
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            rooms = response.json()
            return jsonify({
                'success': True,
                'rooms': rooms
            })
        else:
            return jsonify({
                'success': False,
                'error': f'ChatWork API エラー: {response.status_code}',
                'details': response.text
            }), 500
            
    except requests.exceptions.RequestException as e:
        return jsonify({
            'success': False,
            'error': f'ChatWork API接続エラー: {str(e)}'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'予期しないエラー: {str(e)}'
        }), 500

