#!/usr/bin/env python3
import requests
import json

# Supabase設定
SUPABASE_URL = "https://yyoixwdljeoxtieeazfo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl5b2l4d2RsamVveHRpZWVhemZvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MzkyNjc1NCwiZXhwIjoyMDY5NTAyNzU0fQ.pSr3zahEuvaBJy-HBy85XYUkR-8YUDA0JE6P65y30GY"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def update_item_by_name_and_store(name, store, current_stock, notes=None):
    """アイテム名と店舗名で特定して在庫を更新"""
    url = f"{SUPABASE_URL}/rest/v1/inventory_items"
    params = {
        "name": f"eq.{name}",
        "store": f"eq.{store}"
    }
    
    data = {"current_stock": current_stock}
    if notes:
        data["notes"] = notes
    
    response = requests.patch(url, headers=headers, params=params, json=data)
    if response.status_code == 204:
        print(f"✅ 更新成功: {store} - {name} → {current_stock}")
    else:
        print(f"❌ 更新失敗: {store} - {name} → {response.status_code}: {response.text}")

def delete_item_by_name(name):
    """アイテム名で削除"""
    url = f"{SUPABASE_URL}/rest/v1/inventory_items"
    params = {"name": f"eq.{name}"}
    
    response = requests.delete(url, headers=headers, params=params)
    if response.status_code == 204:
        print(f"✅ 削除成功: {name}")
    else:
        print(f"❌ 削除失敗: {name} → {response.status_code}: {response.text}")

def update_store_name(old_name, new_name):
    """店舗名を一括更新"""
    url = f"{SUPABASE_URL}/rest/v1/inventory_items"
    params = {"store": f"eq.{old_name}"}
    data = {"store": new_name}
    
    response = requests.patch(url, headers=headers, params=params, json=data)
    if response.status_code == 204:
        print(f"✅ 店舗名更新成功: {old_name} → {new_name}")
    else:
        print(f"❌ 店舗名更新失敗: {old_name} → {new_name} → {response.status_code}: {response.text}")

# メイン処理
print("🔄 在庫データベース更新開始...")

# 1. 店舗名変更
print("\n📝 店舗名変更...")
update_store_name("nogneun", "ノンヌン")

# 2. メロン削除
print("\n🗑️ メロン削除...")
delete_item_by_name("メロン")

# 3. Melt店舗の在庫更新
print("\n🏪 Melt店舗の在庫更新...")

# スジャータ
update_item_by_name_and_store("いちごアイス", "Melt", 0)
update_item_by_name_and_store("チョコレートアイス", "Melt", 1.5)
update_item_by_name_and_store("バニラアイス(Melt)", "Melt", 3)
update_item_by_name_and_store("ミルクレープ", "Melt", 3)
update_item_by_name_and_store("牛乳(Melt)", "Melt", 4.5)
update_item_by_name_and_store("ホイップ(Melt)", "Melt", 4)

# ノンヌン
update_item_by_name_and_store("チーズケーキ", "Melt", "1本＋カット1")
update_item_by_name_and_store("ブラウニー", "Melt", "3本＋カット7")
update_item_by_name_and_store("カップケーキ", "Melt", 9)
update_item_by_name_and_store("シフォンケーキ", "Melt", 0.5)
update_item_by_name_and_store("氷", "Melt", 4)

# エープライス
update_item_by_name_and_store("いちごソース(バナナスプリット用)", "Melt", 2)
update_item_by_name_and_store("チョコソース", "Melt", 3)
update_item_by_name_and_store("練乳(Melt)", "Melt", 3)
update_item_by_name_and_store("バタフライピー(Melt)", "Melt", 1.5)

# ライフ
update_item_by_name_and_store("コーヒー(Melt)", "Melt", 1)
update_item_by_name_and_store("ココア(Melt)", "Melt", 3.5)
update_item_by_name_and_store("ホワイトチョコ", "Melt", 8)
update_item_by_name_and_store("ミルクティー(Melt)", "Melt", 4.5)
update_item_by_name_and_store("バナナ", "Melt", 5, "結構傷んできてます")

# 4. ノンヌン店舗の在庫更新
print("\n🏪 ノンヌン店舗の在庫更新...")

# スジャータ
update_item_by_name_and_store("生クリーム", "ノンヌン", 1)
update_item_by_name_and_store("ホイップ", "ノンヌン", 4)
update_item_by_name_and_store("牛乳", "ノンヌン", 3)
update_item_by_name_and_store("バニラアイス", "ノンヌン", 2)

# ライフ
update_item_by_name_and_store("イチゴミルク", "ノンヌン", 0)
update_item_by_name_and_store("練乳", "ノンヌン", 0.5)
update_item_by_name_and_store("ココアパウダー", "ノンヌン", 2)
update_item_by_name_and_store("ゼラチン", "ノンヌン", 0)
update_item_by_name_and_store("コーンフレーク", "ノンヌン", 0.5)
update_item_by_name_and_store("コーヒー", "ノンヌン", 0)
update_item_by_name_and_store("ミルクティー", "ノンヌン", 1)
update_item_by_name_and_store("ココア", "ノンヌン", 1)
update_item_by_name_and_store("卵", "ノンヌン", 0.5)
update_item_by_name_and_store("オレンジジュース", "ノンヌン", 1)
update_item_by_name_and_store("三ツ矢サイダー", "ノンヌン", 4)

# エープライス
update_item_by_name_and_store("ブルーキュラソー", "ノンヌン", 4)
update_item_by_name_and_store("バタフライピー", "ノンヌン", 3)
update_item_by_name_and_store("薄力粉", "ノンヌン", 2)
update_item_by_name_and_store("クリームチーズ", "ノンヌン", 3)
update_item_by_name_and_store("いちごソース(パフェ用)", "ノンヌン", 0.5)
update_item_by_name_and_store("グラニュー糖", "ノンヌン", 5)
update_item_by_name_and_store("ベイキングパウダー", "ノンヌン", 2)
update_item_by_name_and_store("コンスターチ", "ノンヌン", "大量")

print("\n✅ 在庫データベース更新完了！")

