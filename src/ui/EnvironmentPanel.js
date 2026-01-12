export class EnvironmentPanel {
    constructor(uimanager) {
        this.ui = uimanager;
        this.state = {
            windSpeed: 2.0,
            windAngle: 0,
            greenSpeed: 'normal',
            slope: 'mid',
            ground: 'normal'
        };
        this.init();
    }

    init() {
        // 바람 다이얼 클릭/드래그 (단순화된 가상 구현)
        const dial = document.getElementById('wind-dial');
        dial.addEventListener('click', () => {
            this.state.windAngle = (this.state.windAngle + 45) % 360;
            this.updateUI();
        });

        // 토글 그룹 이벤트
        this.bindToggle('green-speed-toggle', 'greenSpeed');
        this.bindToggle('slope-toggle', 'slope');
    }

    bindToggle(id, stateKey) {
        const container = document.getElementById(id);
        const buttons = container.querySelectorAll('button');
        buttons.forEach(btn => {
            btn.addEventListener('click', () => {
                buttons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                this.state[stateKey] = btn.dataset.val;
                console.log(`환경 변경: ${stateKey} -> ${this.state[stateKey]}`);
                // TODO: 물리 엔진에 즉시 반영
            });
        });
    }

    updateUI() {
        const arrow = document.querySelector('.dial-hand');
        if (arrow) arrow.style.transform = `rotate(${this.state.windAngle}deg)`;

        // HUD 동기화
        const hudArrow = document.getElementById('wind-arrow');
        if (hudArrow) hudArrow.style.transform = `rotate(${this.state.windAngle}deg)`;
    }
}
