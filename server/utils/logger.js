import sqlite3 from 'sqlite3';
const db = new sqlite3.Database('./server/db/airswing.db');

export const logSystemAction = (userId, action, details, level = 'info') => {
    const query = `
        INSERT INTO system_logs (user_id, action, details, level) 
        VALUES (?, ?, ?, ?)
    `;
    db.run(query, [userId, action, typeof details === 'object' ? JSON.stringify(details) : details, level], (err) => {
        if (err) console.error('[Logger Error]', err);
    });
};

export const securityAudit = (req, action, details) => {
    const ip = req.headers['x-forwarded-for'] || req.socket.remoteAddress;
    logSystemAction(req.user?.id || 0, action, { ...details, ip }, 'warn');
};
