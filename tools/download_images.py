#!/usr/bin/env python3
"""
いらすとや画像ダウンローダー v2

使い方:
    python download_images.py

必要なパッケージ:
    pip install requests beautifulsoup4

出力:
    - downloads/[ひらがな]/ フォルダに画像を保存
    - download_report.csv に結果を記録
"""

import os
import csv
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 設定
CSV_FILE = "image-candidates.csv"
OUTPUT_DIR = "downloads"
REPORT_FILE = "download_report.csv"
DELAY_SECONDS = 1.5  # リクエスト間の待機時間（サーバー負荷軽減）

# User-Agent（礼儀正しいスクレイピング）
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def get_image_url_from_irasutoya(page_url):
    """
    いらすとやのページから画像URLを抽出
    """
    try:
        response = requests.get(page_url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 方法1: entry-content 内の最初の blogspot 画像
        content_div = soup.find("div", class_="entry-content")
        if content_div:
            img_tags = content_div.find_all("img")
            for img in img_tags:
                src = img.get("src", "")
                if "bp.blogspot.com" in src or "blogger.googleusercontent.com" in src:
                    # 大きいサイズに変換
                    src = convert_to_large_image(src)
                    return src
        
        # 方法2: separator クラス内
        separator = soup.find("div", class_="separator")
        if separator:
            img = separator.find("img")
            if img:
                src = img.get("src", "")
                if src:
                    return convert_to_large_image(src)
        
        # 方法3: og:image メタタグ
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            return og_image["content"]
        
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"    ⚠️ ネットワークエラー: {e}")
        return None
    except Exception as e:
        print(f"    ⚠️ パースエラー: {e}")
        return None


def convert_to_large_image(url):
    """
    画像URLを大きいサイズに変換
    いらすとやの画像は /s400/, /s320/ などのサイズ指定がある
    """
    # s数字 パターンを s800 に置換
    import re
    # /s数字/ または /s数字-c/ パターンを検出
    pattern = r'/s\d+(-c)?/'
    if re.search(pattern, url):
        return re.sub(pattern, '/s800/', url)
    return url


def download_image(image_url, save_path):
    """
    画像をダウンロードして保存
    """
    try:
        response = requests.get(image_url, headers=HEADERS, timeout=30, stream=True)
        response.raise_for_status()
        
        # Content-Type チェック
        content_type = response.headers.get('content-type', '')
        if 'image' not in content_type:
            print(f"    ⚠️ 画像ではありません: {content_type}")
            return False
        
        # ディレクトリ作成
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # 画像保存
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # ファイルサイズ確認
        size_kb = os.path.getsize(save_path) / 1024
        print(f"    📁 保存完了: {size_kb:.1f} KB")
        
        return True
        
    except Exception as e:
        print(f"    ❌ ダウンロードエラー: {e}")
        return False


def main():
    print("=" * 65)
    print("  🎨 いらすとや画像ダウンローダー v2")
    print("=" * 65)
    
    # CSVファイル読み込み
    if not os.path.exists(CSV_FILE):
        print(f"\n❌ エラー: {CSV_FILE} が見つかりません")
        print("   このスクリプトは tools/ フォルダ内で実行してください")
        print("\n   cd tools")
        print("   python download_images.py")
        return
    
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    # 統計情報
    unique_words = len(set((r["hiragana"], r["reading"]) for r in rows))
    print(f"\n📊 {len(rows)} 件の候補（{unique_words} 単語分）を処理します\n")
    print("-" * 65)
    
    # 結果記録
    results = []
    success_count = 0
    fail_count = 0
    
    for i, row in enumerate(rows, 1):
        hiragana = row["hiragana"]
        reading = row["reading"]
        priority = row["priority"]
        page_url = row["page_url"]
        filename = row["filename"]
        description = row.get("description", "")
        
        print(f"\n[{i:02d}/{len(rows)}] 「{reading}」 候補{priority}")
        print(f"    📝 {description}")
        print(f"    🔗 {page_url[:50]}...")
        
        # 画像URL取得
        image_url = get_image_url_from_irasutoya(page_url)
        
        if image_url:
            # 保存パス
            save_path = os.path.join(OUTPUT_DIR, hiragana, filename)
            
            # ダウンロード
            success = download_image(image_url, save_path)
            
            if success:
                print(f"    ✅ {save_path}")
                status = "success"
                success_count += 1
            else:
                status = "download_failed"
                fail_count += 1
        else:
            print(f"    ❌ 画像URL取得失敗")
            status = "url_not_found"
            image_url = ""
            fail_count += 1
        
        results.append({
            "hiragana": hiragana,
            "reading": reading,
            "priority": priority,
            "description": description,
            "page_url": page_url,
            "image_url": image_url or "",
            "filename": filename,
            "status": status,
            "timestamp": datetime.now().isoformat()
        })
        
        # サーバー負荷軽減のため待機
        time.sleep(DELAY_SECONDS)
    
    # レポート保存
    print("\n" + "-" * 65)
    print("📄 レポート保存中...")
    
    with open(REPORT_FILE, "w", encoding="utf-8", newline="") as f:
        fieldnames = ["hiragana", "reading", "priority", "description", "status", "filename", "page_url", "image_url", "timestamp"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    # サマリー
    print("\n" + "=" * 65)
    print("  📊 ダウンロード完了サマリー")
    print("=" * 65)
    print(f"\n    ✅ 成功: {success_count} 件")
    print(f"    ❌ 失敗: {fail_count} 件")
    print(f"    📈 成功率: {success_count/(success_count+fail_count)*100:.1f}%")
    print(f"\n    📁 画像フォルダ: {OUTPUT_DIR}/")
    print(f"    📄 レポート: {REPORT_FILE}")
    
    print("\n" + "=" * 65)
    print("  📋 次のステップ")
    print("=" * 65)
    print(f"""
    1. {OUTPUT_DIR}/ フォルダを開いて画像を確認
    
    2. 各単語につき1つを選定（選定基準）:
       ✅ シンプルで分かりやすい
       ✅ 幼児が認識しやすい
       ✅ カラフルで興味を引く
    
    3. 選定した画像を ../images/[ひらがな]/ にコピー
       例: cp downloads/e/ehon_01.png ../images/e/ehon.png
    
    4. ../data/words.js の image パスを更新
       "placeholder:" → "images/e/ehon.png"
    
    5. Git にコミット & プッシュ
""")


if __name__ == "__main__":
    main()
