from src.models.user import db
from datetime import datetime

class InventoryItem(db.Model):
    __tablename__ = 'inventory_items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    current_stock = db.Column(db.Float, nullable=False, default=0)
    min_stock = db.Column(db.Float, nullable=False, default=0)
    unit = db.Column(db.String(20), nullable=False, default='個')
    order_qty = db.Column(db.Float, nullable=False, default=1)
    supplier = db.Column(db.String(100), nullable=True)
    note = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'current': self.current_stock,
            'min': self.min_stock,
            'unit': self.unit,
            'orderQty': self.order_qty,
            'supplier': self.supplier,
            'note': self.note,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get('name'),
            category=data.get('category'),
            current_stock=data.get('current', 0),
            min_stock=data.get('min', 0),
            unit=data.get('unit', '個'),
            order_qty=data.get('orderQty', 1),
            supplier=data.get('supplier'),
            note=data.get('note')
        )

class StockHistory(db.Model):
    __tablename__ = 'stock_history'
    
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('inventory_items.id'), nullable=False)
    change_amount = db.Column(db.Float, nullable=False)
    previous_stock = db.Column(db.Float, nullable=False)
    new_stock = db.Column(db.Float, nullable=False)
    reason = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    item = db.relationship('InventoryItem', backref=db.backref('history', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'item_id': self.item_id,
            'change_amount': self.change_amount,
            'previous_stock': self.previous_stock,
            'new_stock': self.new_stock,
            'reason': self.reason,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

