export class PaymentUI {
    constructor(ui) {
        this.ui = ui;
        this.modal = document.getElementById('payment-modal');
        this.closeBtn = this.modal.querySelector('.close-btn');
        this.checkoutBtn = document.getElementById('checkout-btn');

        this.bindEvents();
    }

    bindEvents() {
        this.closeBtn.addEventListener('click', () => this.hide());
        this.checkoutBtn.addEventListener('click', () => this.handleCheckout());
    }

    show() {
        this.modal.classList.remove('hidden');
    }

    hide() {
        this.modal.classList.add('hidden');
    }

    async handleCheckout() {
        const token = localStorage.getItem('token');
        if (!token) {
            alert('로그인이 필요합니다.');
            return;
        }

        try {
            this.checkoutBtn.innerText = 'Processing...';
            this.checkoutBtn.disabled = true;

            const resp = await fetch('/api/payments/checkout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ amount: 9900, plan: 'pro' })
            });
            const data = await resp.json();

            // 시뮬레이션: 2초 후 결제 성공 웹훅 호출
            setTimeout(async () => {
                await fetch('/api/payments/webhook', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ paymentId: data.paymentId, success: true })
                });

                alert('결제가 완료되었습니다! Pro 회원으로 업그레이드되었습니다.');
                window.location.reload();
            }, 2000);

        } catch (e) {
            alert('결제 처리 중 오류가 발생했습니다.');
            this.checkoutBtn.innerText = '지금 시작하기';
            this.checkoutBtn.disabled = false;
        }
    }
}
