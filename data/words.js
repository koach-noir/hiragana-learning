/**
 * ひらがな単語データ
 * 
 * 構造:
 * {
 *   "ひらがな": {
 *     words: [
 *       { reading: "よみがな", image: "images/[ひらがな]/[ファイル名].png", emoji: "絵文字（フォールバック）" }
 *     ]
 *   }
 * }
 * 
 * 画像パス:
 * - 実画像: "images/e/ehon.png"
 * - プレースホルダー: "placeholder:" (emojiが表示される)
 */

const WORD_DATA = {
    "え": {
        words: [
            { reading: "え", image: "placeholder:", emoji: "🎨" },
            { reading: "えほん", image: "placeholder:", emoji: "📖" },
            { reading: "えんぴつ", image: "placeholder:", emoji: "✏️" },
            { reading: "えび", image: "placeholder:", emoji: "🦐" },
            { reading: "えがお", image: "placeholder:", emoji: "😊" },
            { reading: "えぷろん", image: "placeholder:", emoji: "👗" },
            { reading: "えき", image: "placeholder:", emoji: "🚉" },
            { reading: "えんとつ", image: "placeholder:", emoji: "🏭" }
        ]
    },
    "の": {
        words: [
            { reading: "のり", image: "placeholder:", emoji: "🍙" },
            { reading: "のーと", image: "placeholder:", emoji: "📓" },
            { reading: "のこぎり", image: "placeholder:", emoji: "🪚" },
            { reading: "のど", image: "placeholder:", emoji: "🫁" },
            { reading: "のはら", image: "placeholder:", emoji: "🌾" }
        ]
    }
};
