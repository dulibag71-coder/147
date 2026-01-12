import sqlite3 from 'sqlite3';
const db = new sqlite3.Database('./server/db/airswing.db');

// 모든 사용자 목록 조회
export const getAllUsers = (req, res) => {
    db.all(`SELECT id, email, role, subscription, skill_level, created_at FROM users`, [], (err, rows) => {
        if (err) return res.status(500).json({ message: '사용자 목록 조회 실패' });
        res.json(rows);
    });
};

// 모든 결제 내역 조회
export const getAllPayments = (req, res) => {
    db.all(`
        SELECT p.*, u.email 
        FROM payments p 
        JOIN users u ON p.user_id = u.id 
        ORDER BY p.created_at DESC
    `, [], (err, rows) => {
        if (err) return res.status(500).json({ message: '결제 내역 조회 실패' });
        res.json(rows);
    });
};

// 서비스 통계 요약
export const getStats = (req, res) => {
    const stats = {};

    db.get(`SELECT COUNT(*) as count FROM users`, (err, row) => {
        stats.totalUsers = row.count;
        db.get(`SELECT COUNT(*) as count FROM users WHERE subscription = 'pro'`, (err, row) => {
            stats.proUsers = row.count;
            db.get(`SELECT SUM(amount) as total FROM payments WHERE status = 'success'`, (err, row) => {
                stats.totalRevenue = row.total || 0;
                db.get(`SELECT COUNT(*) as count FROM shots`, (err, row) => {
                    stats.totalShots = row.count;
                    res.json(stats);
                });
            });
        });
    });
};
