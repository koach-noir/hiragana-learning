// ひらがな50音（あ行〜わ行）
const HIRAGANA_LIST = [
    'あ', 'い', 'う', 'え', 'お',
    'か', 'き', 'く', 'け', 'こ',
    'さ', 'し', 'す', 'せ', 'そ',
    'た', 'ち', 'つ', 'て', 'と',
    'な', 'に', 'ぬ', 'ね', 'の',
    'は', 'ひ', 'ふ', 'へ', 'ほ',
    'ま', 'み', 'む', 'め', 'も',
    'や', 'ゆ', 'よ',
    'ら', 'り', 'る', 'れ', 'ろ',
    'わ', 'を', 'ん'
];

// 実装済みのひらがな
const IMPLEMENTED = Object.keys(WORD_DATA);

// 学習済み記録（localStorage）
const STORAGE_KEY = 'hiragana-learned';
let learnedSet = new Set(JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'));

// 現在選択中のひらがな
let currentHiragana = IMPLEMENTED[0] || 'え';

// 初期化
document.addEventListener('DOMContentLoaded', () => {
    renderNav();
    renderCards(currentHiragana);
    updateProgress();
});

// ナビゲーション描画
function renderNav() {
    const navScroll = document.getElementById('navScroll');
    navScroll.innerHTML = '';
    
    HIRAGANA_LIST.forEach(h => {
        const btn = document.createElement('button');
        btn.className = 'nav-btn';
        btn.textContent = h;
        
        // 実装済みかチェック
        if (!IMPLEMENTED.includes(h)) {
            btn.classList.add('disabled');
        } else {
            btn.addEventListener('click', () => selectHiragana(h));
        }
        
        // 学習済みマーク
        if (learnedSet.has(h)) {
            btn.classList.add('learned');
        }
        
        // 現在選択中
        if (h === currentHiragana) {
            btn.classList.add('active');
        }
        
        navScroll.appendChild(btn);
    });
    
    // 選択中のボタンまでスクロール
    scrollToActive();
}

// 選択中のボタンまでスクロール
function scrollToActive() {
    const navScroll = document.getElementById('navScroll');
    const activeBtn = navScroll.querySelector('.nav-btn.active');
    if (activeBtn) {
        activeBtn.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
    }
}

// ひらがな選択
function selectHiragana(h) {
    if (!IMPLEMENTED.includes(h)) return;
    
    currentHiragana = h;
    renderNav();
    renderCards(h);
}

// カード描画
function renderCards(hiragana) {
    const centerEl = document.getElementById('centerHiragana');
    const container = document.getElementById('cardsContainer');
    
    centerEl.textContent = hiragana;
    container.innerHTML = '';
    
    const data = WORD_DATA[hiragana];
    if (!data || !data.words) {
        container.innerHTML = '<p style="color: white;">データがありません</p>';
        return;
    }
    
    // シャッフル（オプション）
    const words = shuffleArray([...data.words]);
    
    words.forEach(word => {
        const card = document.createElement('div');
        card.className = 'card';
        card.addEventListener('click', () => toggleLabel(card, word.reading));
        
        // 画像またはプレースホルダー
        if (word.image && !word.image.startsWith('placeholder:')) {
            const img = document.createElement('img');
            img.className = 'card-image';
            img.src = word.image;
            img.alt = word.reading;
            img.loading = 'lazy';
            card.appendChild(img);
        } else {
            // プレースホルダー（絵文字）
            const emoji = document.createElement('span');
            emoji.className = 'placeholder-emoji';
            emoji.textContent = word.emoji || '🖼️';
            card.appendChild(emoji);
        }
        
        // ラベル
        const label = document.createElement('div');
        label.className = 'card-label';
        label.innerHTML = `<span>${word.reading}</span>`;
        card.appendChild(label);
        
        // 読み上げボタン
        const speakBtn = document.createElement('button');
        speakBtn.className = 'speak-btn';
        speakBtn.textContent = '🔊';
        speakBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            speak(word.reading);
        });
        card.appendChild(speakBtn);
        
        container.appendChild(card);
    });
}

// ラベル表示切替
function toggleLabel(card, reading) {
    const label = card.querySelector('.card-label');
    const isShowing = label.classList.toggle('show');
    
    // 表示時に読み上げ
    if (isShowing) {
        speak(reading);
        markAsLearned(currentHiragana);
    }
}

// 音声読み上げ（Web Speech API）
function speak(text) {
    if ('speechSynthesis' in window) {
        // 既存の読み上げをキャンセル
        speechSynthesis.cancel();
        
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'ja-JP';
        utterance.rate = 0.8;
        utterance.pitch = 1.2;
        speechSynthesis.speak(utterance);
    }
}

// 学習済みマーク
function markAsLearned(hiragana) {
    if (!learnedSet.has(hiragana)) {
        learnedSet.add(hiragana);
        localStorage.setItem(STORAGE_KEY, JSON.stringify([...learnedSet]));
        renderNav();
        updateProgress();
    }
}

// 進捗更新
function updateProgress() {
    const total = IMPLEMENTED.length;
    const learned = [...learnedSet].filter(h => IMPLEMENTED.includes(h)).length;
    const percent = total > 0 ? (learned / total) * 100 : 0;
    
    document.getElementById('progressFill').style.width = `${percent}%`;
}

// 配列シャッフル
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}
