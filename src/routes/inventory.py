from flask import Blueprint, request, jsonify
from src.models.inventory import db, InventoryItem, StockHistory
from datetime import datetime

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/inventory', methods=['GET'])
def get_all_inventory():
    """全ての在庫アイテムを取得"""
    try:
        items = InventoryItem.query.all()
        inventory_data = {}
        
        for item in items:
            category = item.category
            if category not in inventory_data:
                inventory_data[category] = []
            inventory_data[category].append(item.to_dict())
        
        return jsonify({
            'success': True,
            'data': inventory_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@inventory_bp.route('/inventory/<int:item_id>', methods=['GET'])
def get_inventory_item(item_id):
    """特定の在庫アイテムを取得"""
    try:
        item = InventoryItem.query.get_or_404(item_id)
        return jsonify({
            'success': True,
            'data': item.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@inventory_bp.route('/inventory', methods=['POST'])
def create_inventory_item():
    """新しい在庫アイテムを作成"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'データが提供されていません'
            }), 400
        
        item = InventoryItem.from_dict(data)
        db.session.add(item)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': item.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@inventory_bp.route('/inventory/<int:item_id>/update-stock', methods=['POST'])
def update_stock(item_id):
    """在庫数を更新"""
    try:
        data = request.get_json()
        if not data or 'change' not in data:
            return jsonify({
                'success': False,
                'error': '変更量が指定されていません'
            }), 400
        
        item = InventoryItem.query.get_or_404(item_id)
        change_amount = float(data['change'])
        previous_stock = item.current_stock
        new_stock = max(0, previous_stock + change_amount)
        
        # 在庫履歴を記録
        history = StockHistory(
            item_id=item.id,
            change_amount=change_amount,
            previous_stock=previous_stock,
            new_stock=new_stock,
            reason=data.get('reason', '手動更新')
        )
        
        item.current_stock = new_stock
        item.updated_at = datetime.utcnow()
        
        db.session.add(history)
        db.session.commit()
        
        # 在庫アラートのチェック
        alerts = []
        if new_stock <= 0:
            alerts.append({
                'type': 'out_of_stock',
                'message': f'{item.name}が在庫切れになりました！',
                'item': item.to_dict()
            })
        elif previous_stock > item.min_stock and new_stock <= item.min_stock:
            alerts.append({
                'type': 'low_stock',
                'message': f'{item.name}の在庫が最低値を下回りました！',
                'item': item.to_dict()
            })
        
        return jsonify({
            'success': True,
            'data': item.to_dict(),
            'alerts': alerts,
            'history': history.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@inventory_bp.route('/inventory/<int:item_id>', methods=['PUT'])
def update_inventory_item(item_id):
    """在庫アイテムの情報を更新"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'データが提供されていません'
            }), 400
        
        item = InventoryItem.query.get_or_404(item_id)
        
        # 更新可能なフィールドを更新
        if 'name' in data:
            item.name = data['name']
        if 'category' in data:
            item.category = data['category']
        if 'min' in data:
            item.min_stock = float(data['min'])
        if 'unit' in data:
            item.unit = data['unit']
        if 'orderQty' in data:
            item.order_qty = float(data['orderQty'])
        if 'supplier' in data:
            item.supplier = data['supplier']
        if 'note' in data:
            item.note = data['note']
        
        item.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': item.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@inventory_bp.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_inventory_item(item_id):
    """在庫アイテムを削除"""
    try:
        item = InventoryItem.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{item.name}を削除しました'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@inventory_bp.route('/inventory/stats', methods=['GET'])
def get_inventory_stats():
    """在庫統計情報を取得"""
    try:
        total_items = InventoryItem.query.count()
        low_stock_items = InventoryItem.query.filter(
            InventoryItem.current_stock <= InventoryItem.min_stock,
            InventoryItem.current_stock > 0
        ).count()
        out_of_stock_items = InventoryItem.query.filter(
            InventoryItem.current_stock <= 0
        ).count()
        
        return jsonify({
            'success': True,
            'data': {
                'total_items': total_items,
                'low_stock_count': low_stock_items,
                'out_of_stock_count': out_of_stock_items
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@inventory_bp.route('/inventory/history/<int:item_id>', methods=['GET'])
def get_item_history(item_id):
    """特定アイテムの在庫履歴を取得"""
    try:
        item = InventoryItem.query.get_or_404(item_id)
        history = StockHistory.query.filter_by(item_id=item_id).order_by(
            StockHistory.created_at.desc()
        ).limit(50).all()
        
        return jsonify({
            'success': True,
            'data': {
                'item': item.to_dict(),
                'history': [h.to_dict() for h in history]
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@inventory_bp.route('/inventory/initialize', methods=['POST'])
def initialize_inventory():
    """初期在庫データを設定"""
    try:
        # 既存のデータをクリア
        InventoryItem.query.delete()
        StockHistory.query.delete()
        
        # 初期データ
        initial_data = {
            'sujata': [
                {'name': '生クリーム', 'current': 1, 'min': 1, 'unit': '本', 'orderQty': 4},
                {'name': 'ホイップ', 'current': 2, 'min': 2, 'unit': '本', 'orderQty': 4},
                {'name': '牛乳', 'current': 2, 'min': 2, 'unit': '本', 'orderQty': 5},
                {'name': 'バニラアイス', 'current': 1.5, 'min': 1.5, 'unit': '個', 'orderQty': 2}
            ],
            'life': [
                {'name': 'イチゴミルク', 'current': 1, 'min': 1, 'unit': '本', 'orderQty': 1},
                {'name': '練乳', 'current': 1, 'min': 1, 'unit': '本', 'orderQty': 1},
                {'name': 'ココアパウダー', 'current': 1, 'min': 1, 'unit': '本', 'orderQty': 1},
                {'name': 'ゼラチン', 'current': 1, 'min': 1, 'unit': '本', 'orderQty': 1},
                {'name': 'コーンフレーク', 'current': 1, 'min': 1, 'unit': '本', 'orderQty': 1},
                {'name': 'メロン', 'current': 1, 'min': 1, 'unit': '本', 'orderQty': 1},
                {'name': 'コーヒー', 'current': 0.5, 'min': 1, 'unit': '本', 'orderQty': 1},
                {'name': 'ミルクティー', 'current': 3, 'min': 1, 'unit': '本', 'orderQty': 1},
                {'name': 'ココア', 'current': 1, 'min': 1, 'unit': '本', 'orderQty': 1},
                {'name': '卵', 'current': 1, 'min': 1, 'unit': '本', 'orderQty': 1},
                {'name': 'オレンジジュース', 'current': 1, 'min': 1, 'unit': '本', 'orderQty': 1},
                {'name': '三ツ矢サイダー', 'current': 3, 'min': 3, 'unit': '本', 'orderQty': 1},
                {'name': 'ホワイトチョコ', 'current': 1, 'min': 1, 'unit': '枚', 'orderQty': 1}
            ],
            'aprice': [
                {'name': 'ブルーキュラソー', 'current': 0.33, 'min': 0.33, 'unit': '本', 'orderQty': 1},
                {'name': 'バタフライピー', 'current': 1, 'min': 1, 'unit': '本', 'orderQty': 1},
                {'name': '練乳', 'current': 0.5, 'min': 1, 'unit': '本', 'orderQty': 1},
                {'name': '薄力粉', 'current': 1, 'min': 1, 'unit': '個', 'orderQty': 1},
                {'name': 'クリームチーズ', 'current': 1, 'min': 1, 'unit': '個', 'orderQty': 1},
                {'name': 'いちごソース(パフェ用)', 'current': 1, 'min': 1, 'unit': '個', 'orderQty': 1},
                {'name': 'グラニュー糖', 'current': 1, 'min': 1, 'unit': '個', 'orderQty': 1},
                {'name': 'ベイキングパウダー', 'current': 1, 'min': 1, 'unit': '個', 'orderQty': 1},
                {'name': 'コンスターチ', 'current': 1, 'min': 1, 'unit': '個', 'orderQty': 1},
                {'name': 'いちごソース(バナナスプリット用)', 'current': 0.5, 'min': 1, 'unit': '本', 'orderQty': 1},
                {'name': 'チョコソース', 'current': 0.5, 'min': 1, 'unit': '本', 'orderQty': 1}
            ],
            'melt': [
                {'name': 'いちごアイス', 'current': 1, 'min': 1, 'unit': '個', 'orderQty': 1},
                {'name': 'チョコレートアイス', 'current': 1, 'min': 1, 'unit': '個', 'orderQty': 1},
                {'name': 'バニラアイス', 'current': 2, 'min': 2, 'unit': '個', 'orderQty': 1},
                {'name': 'ミルクレープ', 'current': 2, 'min': 2, 'unit': '箱', 'orderQty': 1},
                {'name': '牛乳', 'current': 3, 'min': 3, 'unit': '本', 'orderQty': 1},
                {'name': 'ホイップ', 'current': 3, 'min': 3, 'unit': '本', 'orderQty': 1},
                {'name': 'チーズケーキ', 'current': 2, 'min': 2, 'unit': '本', 'orderQty': 1},
                {'name': 'ブラウニー', 'current': 2, 'min': 2, 'unit': '本', 'orderQty': 1},
                {'name': 'カップケーキ', 'current': 5, 'min': 5, 'unit': '個', 'orderQty': 1},
                {'name': 'シフォンケーキ', 'current': 0.5, 'min': 0.5, 'unit': '個', 'orderQty': 1},
                {'name': '氷', 'current': 2, 'min': 2, 'unit': '袋', 'orderQty': 1}
            ],
            'other': [
                {'name': 'リボンストロー', 'current': 10, 'min': 10, 'unit': '本', 'orderQty': 10, 'supplier': 'Shein'},
                {'name': 'リボン', 'current': 20, 'min': 20, 'unit': '個', 'orderQty': 20, 'supplier': 'Shein'},
                {'name': 'ハートスポイト', 'current': 30, 'min': 30, 'unit': '個', 'orderQty': 30, 'supplier': 'Shein'},
                {'name': 'ロータスクッキー', 'current': 1, 'min': 1, 'unit': '箱', 'orderQty': 1, 'supplier': 'Amazon'},
                {'name': 'フリーズいちご', 'current': 0.33, 'min': 0.33, 'unit': '袋', 'orderQty': 1, 'supplier': 'Amazon'},
                {'name': '目のチョコ', 'current': 1, 'min': 1, 'unit': '袋', 'orderQty': 1, 'supplier': 'Amazon'},
                {'name': 'バナナ', 'current': 5, 'min': 3, 'unit': '本', 'orderQty': 10, 'supplier': 'ライフ', 'note': '腐り具合要確認'}
            ]
        }
        
        # データベースに追加
        for category, items in initial_data.items():
            for item_data in items:
                item_data['category'] = category
                item = InventoryItem.from_dict(item_data)
                db.session.add(item)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '初期在庫データを設定しました'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

