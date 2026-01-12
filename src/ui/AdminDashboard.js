export class AdminDashboard {
    constructor(ui) {
        this.ui = ui;
        this.element = document.getElementById('admin-dashboard');
        this.closeBtn = document.getElementById('admin-close');
        this.tabBtns = this.element.querySelectorAll('nav button[data-tab]');
        this.contentArea = document.getElementById('admin-tab-content');

        this.bindEvents();
    }

    bindEvents() {
        this.closeBtn.addEventListener('click', () => this.hide());
        this.tabBtns.forEach(btn => {
            btn.addEventListener('click', (e) => this.switchTab(e.target.dataset.tab));
        });
    }

    async show() {
        this.element.classList.remove('hidden');
        await this.loadStats();
    }

    hide() {
        this.element.classList.add('hidden');
    }

    async switchTab(tab) {
        this.tabBtns.forEach(btn => btn.classList.toggle('active', btn.dataset.tab === tab));

        if (tab === 'stats') {
            await this.loadStats();
        } else if (tab === 'users') {
            await this.loadUsers();
        } else if (tab === 'payments') {
            await this.loadPayments();
        } else if (tab === 'centers') {
            await this.loadCenters();
        }
    }

    async loadStats() {
        const token = localStorage.getItem('token');
        try {
            const resp = await fetch('/api/admin/stats', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const stats = await resp.json();

            document.getElementById('stat-total-users').innerText = stats.totalUsers;
            document.getElementById('stat-pro-users').innerText = stats.proUsers;
            document.getElementById('stat-revenue').innerText = stats.totalRevenue.toLocaleString();
            document.getElementById('stat-total-shots').innerText = stats.totalShots;
        } catch (e) {
            console.error('Stats loading failed', e);
        }
    }

    async loadUsers() {
        const token = localStorage.getItem('token');
        try {
            const resp = await fetch('/api/admin/users', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const users = await resp.json();

            this.contentArea.innerHTML = `
                <table class="admin-table">
                    <thead>
                        <tr><th>ID</th><th>Email</th><th>Role</th><th>Subs</th><th>Action</th></tr>
                    </thead>
                    <tbody>
                        ${users.map(u => `
                            <tr>
                               <td>${u.id}</td>
                               <td>${u.email}</td>
                               <td>${u.role}</td>
                               <td>${u.subscription}</td>
                               <td><button class="small-btn">Edit</button></td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
        } catch (e) {
            this.contentArea.innerHTML = '<p>Error loading users</p>';
        }
    }

    async loadPayments() {
        // Similar to loadUsers, fetch /api/admin/payments and render table
    }

    async loadCenters() {
        this.contentArea.innerHTML = `
            <div class="b2b-header">
                <h3>Center Management (B2B Mode)</h3>
                <button class="cta-btn small">Add New Center</button>
            </div>
            <div class="center-grid">
                <div class="center-card">
                    <h4>강남 본점</h4>
                    <p>Active Bays: 12 / 15</p>
                    <p>Status: <span class="badge green">NORMAL</span></p>
                    <button class="small-btn">Manage Bays</button>
                </div>
                <div class="center-card">
                    <h4>판교 센터</h4>
                    <p>Active Bays: 8 / 10</p>
                    <p>Status: <span class="badge yellow">MAINTENANCE</span></p>
                    <button class="small-btn">Manage Bays</button>
                </div>
            </div>
        `;
    }
}
