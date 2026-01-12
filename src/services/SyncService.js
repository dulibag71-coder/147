export class SyncService {
    constructor() {
        this.gameState = {
            user: null,
            inventory: { equippedBall: 'standard' },
            score: [],
            currentHole: 1,
        };
        this.subscribers = [];

        // 로컬 스토리지 이벤트 리스너 (앱 <-> 게임 통신용)
        window.addEventListener('storage', (e) => {
            if (e.key === 'airswing_app_action') {
                this.handleAppAction(JSON.parse(e.newValue));
            }
        });
    }

    // 앱에서의 액션 처리
    handleAppAction(action) {
        if (!action || !action.type) return;

        console.log('[SyncService] App Action:', action.type, action.payload);

        switch (action.type) {
            case 'EQUIP_ITEM':
                this.gameState.inventory.equippedBall = action.payload.itemId;
                this.notifySubscribers('inventory_updated', { equippedBall: action.payload.itemId });
                this.showToast(`🎒 아이템 장착: ${action.payload.itemName}`);
                break;

            case 'REMOTE':
                if (action.payload.command === 'mulligan') {
                    this.notifySubscribers('game_command', { command: 'mulligan' });
                    this.showToast('↺ 멀리건 사용!');
                } else if (action.payload.command === 'camera') {
                    this.notifySubscribers('camera_change', { mode: action.payload.mode });
                }
                break;

            case 'ENV_CONTROL':
                this.notifySubscribers('env_update', { type: action.payload.type, value: action.payload.value });
                this.showToast(`🌬️ 바람 세기 변경: ${action.payload.value}m/s`);
                break;

            case 'CADDY_SETTING':
                this.notifySubscribers('caddy_update', { voice: action.payload.voice });
                this.showToast('🗣️ 캐디 목소리 변경됨');
                break;

            case 'CADDY_SETTING':
                this.notifySubscribers('caddy_update', { voice: action.payload.voice });
                this.showToast('🗣️ 캐디 목소리 변경됨');
                break;

            case 'GOD_MODE':
                this.notifySubscribers('god_mode', { enabled: true });
                this.showToast('⚡ GOD MODE ACTIVATED! (Gravity: Low, Power: MAX)');
                break;

            case 'QR_LOGIN':
                this.notifySubscribers('login_success', action.payload);
                this.showToast(`🔑 [GolfUniverse] ${action.payload.userId}님 환영합니다!`);
                break;
        }
    }

    // 게임 상태 업데이트 (샷 데이터 등)
    updateShotData(shotData) {
        this.gameState.lastShot = shotData;
        this.syncToApp();
    }

    updateScore(scoreData) {
        this.gameState.score = scoreData;
        this.syncToApp();
    }

    showToast(msg) {
        if (window.app && window.app.ui) {
            window.app.ui.showNotification(msg);
        }
    }

    syncToApp() {
        // 실제로는 API 호출이겠지만, 로컬 시뮬레이션을 위해 localStorage 사용
        localStorage.setItem('airswing_game_state', JSON.stringify(this.gameState));
    }

    subscribe(event, callback) {
        this.subscribers.push({ event, callback });
    }

    notifySubscribers(event, data) {
        this.subscribers.forEach(sub => {
            if (sub.event === event) sub.callback(data);
        });
    }
}
