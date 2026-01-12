import jwt from 'jsonwebtoken';

const SECRET_KEY = process.env.JWT_SECRET || 'airswing-secret-key-2026';

export const authenticateToken = (req, res, next) => {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];

    if (!token) return res.status(401).json({ message: '인증 토큰이 없습니다.' });

    jwt.verify(token, SECRET_KEY, (err, user) => {
        if (err) return res.status(403).json({ message: '유효하지 않은 토큰입니다.' });
        req.user = user;
        next();
    });
};

// 관리자 권한 체크
export const authorizeAdmin = (req, res, next) => {
    if (req.user && req.user.role === 'admin') {
        next();
    } else {
        res.status(403).json({ message: '관리자 권한이 필요합니다.' });
    }
};

// 구독 등급 체크 (Pro 기능 잠금)
export const authorizePro = (req, res, next) => {
    if (req.user && req.user.subscription === 'pro') {
        next();
    } else {
        res.status(403).json({
            message: 'Pro 전용 기능입니다.',
            upgradeUrl: '/payment'
        });
    }
};
