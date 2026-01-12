export class Minimap {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.resize();
    }

    resize() {
        this.canvas.width = this.canvas.clientWidth;
        this.canvas.height = this.canvas.clientHeight;
    }

    draw(gameState) {
        const { ctx, canvas } = this;
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // 1. 홀 지형 그리기 (임시 녹색 배경)
        ctx.fillStyle = '#1a3a1a';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // 2. 페이웨이/그린 가이드 (단순 타원)
        ctx.strokeStyle = 'rgba(255,255,255,0.2)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.ellipse(canvas.width / 2, 50, 20, 30, 0, 0, Math.PI * 2);
        ctx.stroke();

        // 3. 현재 공 위치 (화이트 도트)
        ctx.fillStyle = 'white';
        ctx.beginPath();
        ctx.arc(canvas.width / 2, canvas.height - 50, 4, 0, Math.PI * 2);
        ctx.fill();

        // 4. 공 궤적 예측선 (점선)
        ctx.setLineDash([5, 5]);
        ctx.strokeStyle = 'rgba(201, 255, 0, 0.5)';
        ctx.beginPath();
        ctx.moveTo(canvas.width / 2, canvas.height - 50);
        ctx.lineTo(canvas.width / 2, 100);
        ctx.stroke();
        ctx.setLineDash([]);
    }
}
