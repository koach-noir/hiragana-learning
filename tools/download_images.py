#!/usr/bin/env python3
"""
いらすとや画像ダウンローダー

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
from urllib.parse import urljoin
from datetime import datetime

# 設定
CSV_FILE = "image-candidates.csv"
OUTPUT_DIR = "downloads"
REPORT_FILE = "download_report.csv"
DELAY_SECONDS = 1  # リクエスト間の待機時間（サーバー負荷軽減）

# User-Agent（礼儀正しいスクレイピング）
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def get_image_url_from_irasutoya(page_url):
    """
    いらすとやのページから画像URLを抽出
    """
    try:
        response = requests.get(page_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # いらすとやの画像は通常 .entry-content 内の最初の画像
        # または separator クラス内
        content_div = soup.find("div", class_="entry-content")
        if content_div:
            # 最初の大きな画像を探す
            img_tags = content_div.find_all("img")
            for img in img_tags:
                src = img.get("src", "")
                # bp.blogspot.com の画像URLを探す
                if "bp.blogspot.com" in src:
                    # 大きいサイズに変換（s400 → s800 など）
                    # URLの末尾が /sXXX/ の形式の場合、大きくする
                    if "/s" in src:
                        # s400 を s800 に変更（より大きな画像）
                        parts = src.rsplit("/s", 1)
                        if len(parts) == 2:
                            size_and_rest = parts[1]
                            if "/" in size_and_rest:
                                rest = size_and_rest.split("/", 1)[1]
                                src = f"{parts[0]}/s800/{rest}"
                    return src
        
        # 代替: og:image メタタグから取得
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            return og_image["content"]
        
        return None
        
    except Exception as e:
        print(f"  エラー: {e}")
        return None


def download_image(image_url, save_path):
    """
    画像をダウンロードして保存
    """
    try:
        response = requests.get(image_url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        
        # ディレクトリ作成
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # 画像保存
        with open(save_path, "wb") as f:
            f.write(response.content)
        
        return True
        
    except Exception as e:
        print(f"  ダウンロードエラー: {e}")
        return False


def main():
    print("=" * 60)
    print("いらすとや画像ダウンローダー")
    print("=" * 60)
    
    # CSVファイル読み込み
    if not os.path.exists(CSV_FILE):
        print(f"エラー: {CSV_FILE} が見つかりません")
        print("このスクリプトは tools/ フォルダ内で実行してください")
        return
    
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    print(f"\n{len(rows)} 件の候補を処理します...\n")
    
    # 結果記録
    results = []
    
    for i, row in enumerate(rows, 1):
        hiragana = row["hiragana"]
        reading = row["reading"]
        priority = row["priority"]
        page_url = row["page_url"]
        filename = row["filename"]
        
        print(f"[{i}/{len(rows)}] {reading} (優先度{priority})")
        print(f"  URL: {page_url}")
        
        # 画像URL取得
        image_url = get_image_url_from_irasutoya(page_url)
        
        if image_url:
            print(f"  画像URL: {image_url[:60]}...")
            
            # 保存パス
            save_path = os.path.join(OUTPUT_DIR, hiragana, filename)
            
            # ダウンロード
            success = download_image(image_url, save_path)
            
            if success:
                print(f"  ✅ 保存: {save_path}")
                status = "success"
            else:
                print(f"  ❌ 保存失敗")
                status = "download_failed"
        else:
            print(f"  ❌ 画像URL取得失敗")
            status = "url_not_found"
            image_url = ""
            save_path = ""
        
        results.append({
            "hiragana": hiragana,
            "reading": reading,
            "priority": priority,
            "page_url": page_url,
            "image_url": image_url,
            "filename": filename,
            "status": status,
            "timestamp": datetime.now().isoformat()
        })
        
        # サーバー負荷軽減のため待機
        time.sleep(DELAY_SECONDS)
        print()
    
    # レポート保存
    with open(REPORT_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    
    # サマリー
    print("=" * 60)
    print("ダウンロード完了")
    print("=" * 60)
    
    success_count = sum(1 for r in results if r["status"] == "success")
    failed_count = len(results) - success_count
    
    print(f"  成功: {success_count} 件")
    print(f"  失敗: {failed_count} 件")
    print(f"\n  結果: {REPORT_FILE}")
    print(f"  画像: {OUTPUT_DIR}/ フォルダ")
    print()
    print("次のステップ:")
    print(f"  1. {OUTPUT_DIR}/ フォルダ内の画像を確認")
    print("  2. 各単語につき1つを選定")
    print("  3. 選定した画像を images/ フォルダにコピー")
    print("  4. data/words.js の image パスを更新")


if __name__ == "__main__":
    main()
