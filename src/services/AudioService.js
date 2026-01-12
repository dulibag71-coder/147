export class AudioService {
    constructor() {
        this.synth = window.speechSynthesis;
        this.voices = [];
        this.init();
    }

    init() {
        const loadVoices = () => {
            this.voices = this.synth.getVoices();
        };
        loadVoices();
        if (this.synth.onvoiceschanged !== undefined) {
            this.synth.onvoiceschanged = loadVoices;
        }
    }

    speak(text) {
        if (this.synth.speaking) this.synth.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        // 한국어 여성 목소리 선호 (골프존 캐디 느낌)
        const koVoice = this.voices.find(v => v.lang === 'ko-KR' || v.lang.includes('ko'));
        if (koVoice) utterance.voice = koVoice;

        utterance.pitch = 1.1;
        utterance.rate = 1.0;
        this.synth.speak(utterance);
    }

    playEffect(type) {
        // TODO: Web Audio API를 활용한 샷 임팩트음, 환호성 등 재생
        console.log(`[AudioEffect] -> ${type}`);
    }

    announceDistance(dist) {
        this.speak(`핀까지의 거리는 ${Math.round(dist)}미터입니다.`);
    }

    announceShot(type) {
        const messages = {
            good: "나이스 샷!",
            bunker: "벙커입니다.",
            hazard: "해저드입니다.",
            ob: "오비입니다.",
            ready: "준비해 주세요.",
            impact: "임팩트!"
        };
        if (messages[type]) this.speak(messages[type]);
    }
}
