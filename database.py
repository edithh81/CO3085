import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional

class Database:
    def __init__(self, db_path: str = "orders.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                items TEXT NOT NULL,
                total_price REAL NOT NULL,
                status TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def create_order(self, session_id: str, items: List[Dict], total_price: float) -> int:
        """Create a new order"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO orders (session_id, items, total_price, status)
            VALUES (?, ?, ?, ?)
        """, (session_id, json.dumps(items), total_price, "pending"))
        
        order_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return order_id
    
    def get_order(self, order_id: int) -> Optional[Dict]:
        """Get order by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "id": row[0],
                "session_id": row[1],
                "items": json.loads(row[2]),
                "total_price": row[3],
                "status": row[4],
                "created_at": row[5]
            }
        return None
    
    def cancel_order(self, order_id: int) -> bool:
        """Cancel an order"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE orders SET status = 'cancelled' 
            WHERE id = ? AND status = 'pending'
        """, (order_id,))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def get_session_orders(self, session_id: str) -> List[Dict]:
        """Get all orders for a session"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM orders WHERE session_id = ? 
            ORDER BY created_at DESC
        """, (session_id,))
        
        orders = []
        for row in cursor.fetchall():
            orders.append({
                "id": row[0],
                "session_id": row[1],
                "items": json.loads(row[2]),
                "total_price": row[3],
                "status": row[4],
                "created_at": row[5]
            })
        
        conn.close()
        return orders
