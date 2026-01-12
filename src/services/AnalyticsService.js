export class AnalyticsService {
    constructor() {
        this.endpoint = '/api/analytics/track'; // Placeholder
        this.sessionStartTime = Date.now();
    }

    async track(eventName, properties = {}) {
        const payload = {
            event: eventName,
            properties: {
                ...properties,
                timestamp: new Date().toISOString(),
                url: window.location.href,
                userAgent: navigator.userAgent
            }
        };

        console.log(`[Analytics] ${eventName}`, payload);

        // 상용 운영 시 실제 로그 수집 서버로 전송
        /*
        try {
            await fetch(this.endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
        } catch (e) {}
        */
    }

    trackUserAction(action, details) {
        this.track('user_action', { action, details });
    }

    trackPaymentInit(plan, amount) {
        this.track('payment_init', { plan, amount });
    }

    trackShot(data) {
        this.track('shot_recorded', data);
    }
}

export const analytics = new AnalyticsService();
