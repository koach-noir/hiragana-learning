# 🎨 ひらがなをまなぼう

幼児向けひらがな学習アプリ - タップで学ぶ50音カード

## 🌟 機能

- **横スクロールナビ**: 50音から学びたいひらがなを選択
- **イラストカード**: タップでひらがな読みをオーバーレイ表示
- **音声読み上げ**: Web Speech APIによる発音機能
- **進捗トラッキング**: 学習済みマーク＆進捗バー（localStorage保存）
- **シャッフル**: 毎回ランダム順で表示

## 🚀 クイックスタート

### 必要なもの

- Python 3.x
- pip3
- Git

### セットアップ手順

```bash
# 1. リポジトリをクローン
git clone https://github.com/koach-noir/hiragana-learning.git
cd hiragana-learning

# 2. Python依存パッケージをインストール
pip3 install requests beautifulsoup4

# 3. 画像をダウンロード
cd tools
python3 download_images.py

# 4. ローカルサーバーで起動
cd ..
python3 -m http.server 8000
# ブラウザで http://localhost:8000 にアクセス
```

詳細なセットアップ手順は [SETUP.md](SETUP.md) を参照してください。

## 📁 ファイル構成

```
hiragana-learning/
├── index.html          # メインHTML
├── css/
│   └── style.css       # スタイル
├── js/
│   └── app.js          # アプリロジック
├── data/
│   ├── words.js        # 単語データ
│   └── image-sources.csv  # 画像ダウンロード元URL管理
├── images/             # 画像フォルダ
│   ├── e/              # 「え」の画像
│   └── no/             # 「の」の画像
├── tools/
│   └── download_images.py  # 画像ダウンロードスクリプト
├── README.md           # このファイル
└── SETUP.md            # 詳細なセットアップガイド
```

## 📝 単語データの追加

`data/words.js` に新しいひらがなを追加:

```javascript
const WORD_DATA = {
    "あ": {
        words: [
            { reading: "あめ", image: "images/a/ame.png", emoji: "🍬" },
            // ...
        ]
    },
    // ...
};
```

## 🖼️ 画像の追加方法

### 自動ダウンロード（推奨）

1. `data/image-sources.csv` に画像URLを追加
2. `python3 tools/download_images.py` を実行

### 手動追加

1. `images/[ひらがな]/` フォルダに画像を保存
2. `data/words.js` の `image` パスを更新

## 🌐 GitHub Pagesで公開

1. GitHub リポジトリの **Settings** → **Pages**
2. **Source**: `main` branch を選択
3. **Save** をクリック
4. `https://koach-noir.github.io/hiragana-learning/` でアクセス可能

## 📱 対応環境

- タブレット縦向き最適化
- iOS Safari / Chrome
- Android Chrome
- デスクトップブラウザ

## 🔄 開発状況

- [x] 基本UIの実装
- [x] 「え」「の」の単語データ
- [ ] すべての50音の実装
- [ ] 音声読み上げ機能
- [ ] 進捗トラッキング
- [ ] PWA化

## 🖼️ 画像ソース

- [いらすとや](https://www.irasutoya.com/) - かわいいフリー素材
- [イラストAC](https://www.ac-illust.com/) - 無料イラスト
- [シルエットAC](https://www.silhouette-ac.com/) - シルエット素材

## 📄 ライセンス

MIT License

画像素材は各配布元の利用規約に従ってください。

## 🤝 コントリビューション

IssueやPull Requestは大歓迎です！

1. このリポジトリをFork
2. Feature branchを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をCommit (`git commit -m 'Add amazing feature'`)
4. Branchをpush (`git push origin feature/amazing-feature`)
5. Pull Requestを作成
