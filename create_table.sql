-- 在庫管理テーブルの作成
CREATE TABLE IF NOT EXISTS inventory_items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    current_stock DECIMAL(10,2) NOT NULL DEFAULT 0,
    min_stock DECIMAL(10,2) NOT NULL DEFAULT 1,
    order_qty DECIMAL(10,2) NOT NULL DEFAULT 1,
    unit VARCHAR(20) NOT NULL DEFAULT '個',
    supplier VARCHAR(50) NOT NULL,
    store VARCHAR(50) NOT NULL,
    category VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- RLS (Row Level Security) 設定
ALTER TABLE inventory_items ENABLE ROW LEVEL SECURITY;

-- 全ユーザーに読み取り権限
DROP POLICY IF EXISTS "Allow read access for all users" ON inventory_items;
CREATE POLICY "Allow read access for all users" ON inventory_items
    FOR SELECT USING (true);

-- 全ユーザーに書き込み権限
DROP POLICY IF EXISTS "Allow write access for all users" ON inventory_items;
CREATE POLICY "Allow write access for all users" ON inventory_items
    FOR ALL USING (true);

-- 更新時刻自動更新のトリガー
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

DROP TRIGGER IF EXISTS update_inventory_items_updated_at ON inventory_items;
CREATE TRIGGER update_inventory_items_updated_at 
    BEFORE UPDATE ON inventory_items 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 初期データの投入
INSERT INTO inventory_items (name, current_stock, min_stock, order_qty, unit, supplier, store, category, notes) VALUES
-- nogneun店 - スジャータ仕入先
('生クリーム', 1, 1, 4, '本', 'スジャータ', 'nogneun', '乳製品', NULL),
('ホイップ', 2, 2, 4, '本', 'スジャータ', 'nogneun', '乳製品', NULL),
('牛乳', 2, 2, 5, '本', 'スジャータ', 'nogneun', '乳製品', NULL),
('バニラアイス', 1.5, 1.5, 2, '個', 'スジャータ', 'nogneun', 'アイス', NULL),

-- nogneun店 - ライフ仕入先
('イチゴミルク', 1, 1, 1, '本', 'ライフ', 'nogneun', '飲料', NULL),
('練乳', 1, 1, 1, '本', 'ライフ', 'nogneun', '調味料', NULL),
('ココアパウダー', 1, 1, 1, '本', 'ライフ', 'nogneun', '製菓材料', NULL),
('ゼラチン', 1, 1, 1, '本', 'ライフ', 'nogneun', '製菓材料', NULL),
('コーンフレーク', 1, 1, 1, '本', 'ライフ', 'nogneun', '食材', NULL),
('メロン', 1, 1, 1, '本', 'ライフ', 'nogneun', '飲料', NULL),
('コーヒー', 1, 1, 1, '本', 'ライフ', 'nogneun', '飲料', NULL),
('ミルクティー', 1, 1, 1, '本', 'ライフ', 'nogneun', '飲料', NULL),
('ココア', 1, 1, 1, '本', 'ライフ', 'nogneun', '飲料', NULL),
('卵', 1, 1, 1, '本', 'ライフ', 'nogneun', '食材', NULL),
('オレンジジュース', 1, 1, 1, '本', 'ライフ', 'nogneun', '飲料', NULL),
('三ツ矢サイダー', 3, 3, 1, '本', 'ライフ', 'nogneun', '飲料', NULL),

-- nogneun店 - エープライス仕入先
('ブルーキュラソー', 0.33, 0.33, 1, '本', 'エープライス', 'nogneun', '製菓材料', NULL),
('バタフライピー', 1, 1, 1, '本', 'エープライス', 'nogneun', '製菓材料', NULL),
('練乳(エープライス)', 1, 1, 1, '本', 'エープライス', 'nogneun', '調味料', NULL),
('薄力粉', 1, 1, 1, '個', 'エープライス', 'nogneun', '製菓材料', NULL),
('クリームチーズ', 1, 1, 1, '個', 'エープライス', 'nogneun', '乳製品', NULL),
('いちごソース(パフェ用)', 1, 1, 1, '個', 'エープライス', 'nogneun', 'ソース', NULL),
('グラニュー糖', 1, 1, 1, '個', 'エープライス', 'nogneun', '製菓材料', NULL),
('ベイキングパウダー', 1, 1, 1, '個', 'エープライス', 'nogneun', '製菓材料', NULL),
('コンスターチ', 1, 1, 1, '個', 'エープライス', 'nogneun', '製菓材料', NULL),

-- Melt店 - スジャータ仕入先
('いちごアイス', 1, 1, 1, '個', 'スジャータ', 'Melt', 'アイス', NULL),
('チョコレートアイス', 1, 1, 1, '個', 'スジャータ', 'Melt', 'アイス', NULL),
('バニラアイス(Melt)', 2, 2, 1, '個', 'スジャータ', 'Melt', 'アイス', NULL),
('ミルクレープ', 2, 2, 1, '箱', 'スジャータ', 'Melt', 'デザート', NULL),
('牛乳(Melt)', 3, 3, 1, '本', 'スジャータ', 'Melt', '乳製品', NULL),
('ホイップ(Melt)', 3, 3, 1, '本', 'スジャータ', 'Melt', '乳製品', NULL),

-- Melt店 - ノンヌン仕入先
('チーズケーキ', 2, 2, 1, '本', 'ノンヌン', 'Melt', 'デザート', NULL),
('ブラウニー', 2, 2, 1, '本', 'ノンヌン', 'Melt', 'デザート', NULL),
('カップケーキ', 5, 5, 1, '個', 'ノンヌン', 'Melt', 'デザート', NULL),
('シフォンケーキ', 0.5, 0.5, 1, '個', 'ノンヌン', 'Melt', 'デザート', NULL),
('氷', 2, 2, 1, '袋', 'ノンヌン', 'Melt', '食材', NULL),

-- Melt店 - エープライス仕入先
('いちごソース(バナナスプリット用)', 0.5, 0.5, 1, '本', 'エープライス', 'Melt', 'ソース', NULL),
('チョコソース', 0.5, 0.5, 1, '本', 'エープライス', 'Melt', 'ソース', NULL),
('練乳(Melt)', 0.5, 0.5, 1, '本', 'エープライス', 'Melt', '調味料', NULL),
('バタフライピー(Melt)', 1, 1, 1, '本', 'エープライス', 'Melt', '製菓材料', NULL),

-- Melt店 - ライフ仕入先
('コーヒー(Melt)', 0.5, 0.5, 1, '本', 'ライフ', 'Melt', '飲料', NULL),
('ココア(Melt)', 1, 1, 1, '本', 'ライフ', 'Melt', '飲料', NULL),
('ホワイトチョコ', 1, 1, 1, '枚', 'ライフ', 'Melt', '製菓材料', NULL),
('ミルクティー(Melt)', 3, 3, 1, '本', 'ライフ', 'Melt', '飲料', NULL),
('バナナ', 1, 1, 1, '本', 'ライフ', 'Melt', '果物', '毎回腐り具合と共に報告'),

-- Melt店 - Shein仕入先
('リボンストロー', 10, 10, 1, '本', 'Shein', 'Melt', '装飾品', NULL),
('リボン', 20, 20, 1, '個', 'Shein', 'Melt', '装飾品', NULL),
('ハートスポイト', 30, 30, 1, '個', 'Shein', 'Melt', '装飾品', NULL),

-- Melt店 - Amazon仕入先
('ロータスクッキー', 1, 1, 1, '箱', 'Amazon', 'Melt', '食材', NULL),
('フリーズいちご', 0.33, 0.33, 1, '袋', 'Amazon', 'Melt', '食材', NULL),
('目のチョコ', 1, 1, 1, '袋', 'Amazon', 'Melt', '装飾品', NULL)

ON CONFLICT DO NOTHING;

