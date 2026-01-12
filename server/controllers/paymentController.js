import sqlite3 from 'sqlite3';
const db = new sqlite3.Database('./server/db/airswing.db');

// 결제 요청 (시뮬레이션)
export const createCheckout = (req, res) => {
    const { amount, plan } = req.body;
    const userId = req.user.id;
    const paymentId = `PAY-${Date.now()}-${Math.floor(Math.random() * 1000)}`;

    db.run(`
        INSERT INTO payments (user_id, payment_id, amount, status) 
        VALUES (?, ?, ?, 'pending')
    `, [userId, paymentId, amount], function (err) {
        if (err) return res.status(500).json({ message: '결제 요청 실패' });

        // 실제 환경에서는 PG사 결제창 URL을 반환하겠지만, 여기서는 성공 시뮬레이션용 ID 반환
        res.json({
            message: '결제 세션 생성됨',
            paymentId,
            checkoutUrl: `/simulate-payment?id=${paymentId}`
        });
    });
};

// 결제 완료 처리 (Webhook 시뮬레이션)
export const completePayment = (req, res) => {
    const { paymentId, success } = req.body;

    if (!success) {
        db.run(`UPDATE payments SET status = 'failed' WHERE payment_id = ?`, [paymentId]);
        return res.json({ message: '결제 실패 처리됨' });
    }

    db.get(`SELECT user_id FROM payments WHERE payment_id = ?`, [paymentId], (err, payment) => {
        if (!payment) return res.status(404).json({ message: '결제 정보를 찾을 수 없습니다.' });

        db.serialize(() => {
            // 결제 상태 업데이트
            db.run(`UPDATE payments SET status = 'success' WHERE payment_id = ?`, [paymentId]);

            // 사용자 구독 상태 업데이트 (Pro 등급)
            const startDate = new Date().toISOString();
            const endDate = new Date();
            endDate.setMonth(endDate.getMonth() + 1); // 1개월 구독

            db.run(`
                UPDATE users 
                SET subscription = 'pro', 
                    subscription_start = ?, 
                    subscription_end = ? 
                WHERE id = ?
            `, [startDate, endDate.toISOString(), payment.user_id]);

            // 로그 기록
            db.run(`
                INSERT INTO system_logs (user_id, action, details) 
                VALUES (?, 'payment_success', ?)
            `, [payment.user_id, `Payment ID: ${paymentId}`]);
        });

        res.json({ message: '결제 및 구독 업데이트 완료' });
    });
};
