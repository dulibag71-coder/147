export class ClubSelector {
    constructor(uimanager) {
        this.ui = uimanager;
        this.clubs = [
            { id: 'DR', name: 'DRIVER', dist: 230, loft: 10.5 },
            { id: 'W3', name: 'WOOD 3', dist: 210, loft: 15 },
            { id: 'I5', name: 'IRON 5', dist: 170, loft: 27 },
            { id: 'I7', name: 'IRON 7', dist: 150, loft: 34 },
            { id: 'PW', name: 'PITCHING', dist: 110, loft: 45 },
            { id: 'PT', name: 'PUTTER', dist: 0, loft: 3.5 }
        ];
        this.currentIndex = 0;
        this.init();
    }

    init() {
        window.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowUp') this.prev();
            if (e.key === 'ArrowDown') this.next();
        });
    }

    next() {
        this.currentIndex = (this.currentIndex + 1) % this.clubs.length;
        this.updateUI();
    }

    prev() {
        this.currentIndex = (this.currentIndex - 1 + this.clubs.length) % this.clubs.length;
        this.updateUI();
    }

    updateUI() {
        const current = this.clubs[this.currentIndex];
        const prev = this.clubs[(this.currentIndex - 1 + this.clubs.length) % this.clubs.length];
        const next = this.clubs[(this.currentIndex + 1) % this.clubs.length];

        const wheel = document.getElementById('club-wheel');
        wheel.innerHTML = `
            <div class="club-option prev">${prev.name}</div>
            <div class="club-option active">${current.name}</div>
            <div class="club-option next">${next.name}</div>
        `;

        document.getElementById('current-club-name').innerText = current.name;
        document.getElementById('club-recommend').innerText = `L: ${current.loft}°`;
        document.getElementById('est-dist').innerText = current.dist;

        // 퍼팅 모드 체크
        if (current.id === 'PT') {
            this.ui.app.togglePuttingMode(true);
        } else {
            this.ui.app.togglePuttingMode(false);
        }
    }
}
