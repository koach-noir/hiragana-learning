# 🎨 ひらがなをまなぼう

幼児向けひらがな学習アプリ - タップで学ぶ50音カード

## 🌟 機能

- **横スクロールナビ**: 50音から学びたいひらがなを選択
- **イラストカード**: タップでひらがな読みをオーバーレイ表示
- **音声読み上げ**: Web Speech APIによる発音機能
- **進捗トラッキング**: 学習済みマーク＆進捗バー（localStorage保存）
- **シャッフル**: 毎回ランダム順で表示

## 📁 ファイル構成

```
hiragana-learning/
├── index.html          # メインHTML
├── css/
│   └── style.css       # スタイル
├── js/
│   └── app.js          # アプリロジック
├── data/
│   ├── words.js        # 単語データ（プロジェクト内パス）
│   └── image-sources.csv  # 画像ダウンロード元URL管理
└── images/             # 画像フォルダ（手動追加）
    ├── e/              # 「え」の画像
    └── no/             # 「の」の画像
```

## 🚀 使い方

### 1. GitHub Pagesで公開

Settings → Pages → Source: `main` branch → Save

### 2. 画像の追加方法

1. `data/image-sources.csv` を参照
2. `source_url` からイラストをダウンロード
3. `images/[ひらがな]/` フォルダに保存
4. `data/words.js` の `image` パスを更新
5. `status` を `done` に変更

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

## 🖼️ 画像ソース

- [いらすとや](https://www.irasutoya.com/) - かわいいフリー素材
- [イラストAC](https://www.ac-illust.com/) - 無料イラスト
- [シルエットAC](https://www.silhouette-ac.com/) - シルエット素材

## 📱 対応環境

- タブレット縦向き最適化
- iOS Safari / Chrome
- Android Chrome

## 📄 ライセンス

MIT License

画像素材は各配布元の利用規約に従ってください。
