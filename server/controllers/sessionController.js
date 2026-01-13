export const sessionStore = {}; // { sessionId: { status: 'waiting' | 'connected', userId: null, createdAt: Date } }

export const createSession = (req, res) => {
    // 6자리 난수 or UUID
    const sessionId = Math.random().toString(36).substring(2, 8).toUpperCase();
    sessionStore[sessionId] = {
        status: 'waiting',
        createdAt: Date.now()
    };
    // 5분 후 만료
    setTimeout(() => {
        delete sessionStore[sessionId];
    }, 5 * 60 * 1000);

    res.json({ sessionId });
};

export const checkSession = (req, res) => {
    const { sessionId } = req.query;
    const session = sessionStore[sessionId];

    if (!session) {
        return res.status(404).json({ message: '유효하지 않은 세션입니다.' });
    }

    if (session.status === 'connected') {
        // 세션 완료 -> PC 로그인 처리 (토큰 발급 등은 여기서 안 하고, 클라이언트가 알게 함)
        // 실제로는 여기서 User Detail을 줘서 PC가 토큰을 받게 할 수도 있음.
        // 보안상: 모바일에서 토큰을 넘겨주는 방식 or 여기서 일회용 코드 발급
        // 간단히: User ID 반환
        return res.json({ status: 'connected', userId: session.userId });
    }

    res.json({ status: 'waiting' });
};

export const connectSession = (req, res) => {
    const { sessionId } = req.body;
    const userId = req.user.id; // JWT Auth Middleware 필요

    const session = sessionStore[sessionId];
    if (!session) {
        return res.status(404).json({ message: '세션을 찾을 수 없습니다.' });
    }

    session.status = 'connected';
    session.userId = userId;

    res.json({ message: '연결되었습니다.' });
};
