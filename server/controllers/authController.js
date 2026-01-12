import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import db from '../db/database.js';

const SECRET_KEY = process.env.JWT_SECRET || 'airswing-secret-key-2026';

export const register = (req, res) => {
    const { email, password } = req.body;

    if (!email || !password) {
        return res.status(400).json({ message: '이메일과 비밀번호를 입력해주세요.' });
    }

    const hashedPassword = bcrypt.hashSync(password, 10);

    db.run(`INSERT INTO users (email, password) VALUES (?, ?)`, [email, hashedPassword], function (err) {
        if (err) {
            if (err.message.includes('UNIQUE constraint failed')) {
                return res.status(400).json({ message: '이미 존재하는 이메일입니다.' });
            }
            return res.status(500).json({ message: '회원가입 중 오류가 발생했습니다.' });
        }
        res.status(201).json({ message: '회원가입이 완료되었습니다.', userId: this.lastID });
    });
};

export const login = (req, res) => {
    const { email, password } = req.body;

    db.get(`SELECT * FROM users WHERE email = ?`, [email], (err, user) => {
        if (err) return res.status(500).json({ message: '로그인 중 오류가 발생했습니다.' });
        if (!user) return res.status(400).json({ message: '가입되지 않은 이메일입니다.' });

        const isValid = bcrypt.compareSync(password, user.password);
        if (!isValid) return res.status(400).json({ message: '비밀번호가 일치하지 않습니다.' });

        const token = jwt.sign(
            { id: user.id, email: user.email, subscription: user.subscription, role: user.role },
            SECRET_KEY,
            { expiresIn: '24h' }
        );

        res.json({
            message: '로그인 성공',
            token,
            user: {
                id: user.id,
                email: user.email,
                skillLevel: user.skill_level,
                subscription: user.subscription,
                role: user.role
            }
        });
    });
};
