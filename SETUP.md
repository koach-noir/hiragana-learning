# 環境構築手順（備忘録）

## 🖥️ 開発環境

- **OS**: macOS
- **Python**: Python 3.x（既存インストール）
- **パッケージマネージャー**: pip3

## 📦 初回セットアップ

### 1. リポジトリのクローン

```bash
git clone https://github.com/koach-noir/hiragana-learning.git
cd hiragana-learning
```

### 2. Python依存パッケージのインストール

```bash
pip3 install requests beautifulsoup4
```

**必要なパッケージ**:
- `requests` - HTTP通信用
- `beautifulsoup4` - HTML解析用（画像スクレイピング）

### 3. 画像のダウンロード

```bash
cd tools
python3 download_images.py
```

このスクリプトは `data/image-sources.csv` を読み込み、指定されたURLから画像をダウンロードして `images/` フォルダに保存します。

## 🔧 トラブルシューティング

### Python / pip が見つからない場合

#### Homebrewを使ったインストール

```bash
# Homebrewのインストール（未インストールの場合）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Python 3のインストール
brew install python3

# インストール確認
python3 --version
pip3 --version
```

### 画像ダウンロードスクリプトの問題

- **CSVファイルが見つからない**: `data/image-sources.csv` が存在することを確認
- **画像フォルダがない**: `images/` フォルダが作成されているか確認
- **ネットワークエラー**: インターネット接続を確認

## 📝 日常的なワークフロー

### コードの変更をプッシュ

```bash
git add .
git commit -m "説明文"
git push origin main
```

### 新しいひらがなの追加

1. `data/words.js` に単語データを追加
2. `data/image-sources.csv` に画像URLを追加
3. `python3 tools/download_images.py` で画像をダウンロード
4. 動作確認後、Gitにコミット

### ローカルでのテスト

シンプルなHTTPサーバーを起動:

```bash
# Python 3を使う場合
python3 -m http.server 8000

# ブラウザで http://localhost:8000 にアクセス
```

## 🌐 GitHub Pagesでの公開

1. GitHubリポジトリページにアクセス
2. **Settings** → **Pages**
3. **Source**: `main` branch を選択
4. **Save** をクリック
5. 数分後、`https://koach-noir.github.io/hiragana-learning/` でアクセス可能

## 🔄 今後の拡張

- [ ] すべての50音の単語と画像を追加
- [ ] 音声読み上げ機能の実装
- [ ] 進捗トラッキング機能
- [ ] PWA化（オフライン対応）
- [ ] クイズモード追加

## 📚 参考リソース

- [Python公式ドキュメント](https://docs.python.org/ja/3/)
- [GitHub Pages ドキュメント](https://docs.github.com/ja/pages)
- [いらすとや](https://www.irasutoya.com/) - イラスト素材
