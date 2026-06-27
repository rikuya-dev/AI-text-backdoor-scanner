# AI Text Backdoor Detector

自然言語処理（NLP）の学習データ内(csv)に含まれる「テキスト型バックドア」を検出し、AIモデルの安全性を監査するためのソフトウェアです。

This software detects "text-based backdoors" in training datasets to audit and ensure the safety of NLP models.

---

## 📌 テキスト型バックドアとは (What is a Text-based Backdoor?)

特定の文字列（トリガー）をプロンプトに含めることで、AIモデルの出力を意図的にゆがめる攻撃手法です。本ソフトウェアでは、以下の3種類のテキスト型バックドアの検出に対応しています。

1. **無意味型 (Innocuous/Random Word Trigger)**
   - プロンプトの文脈とは全く関係のない単語を挿入する手法。
2. **不可視型 (Invisible Trigger)**
   - ゼロ幅文字など、人間の目には見えない特殊な文字列を仕込む手法。
3. **自然言語型 (Natural Language Trigger)**
   - プロンプトの文脈に自然に溶け込むような単語を巧妙に配置する手法。

---

## 🛠️ 検出アルゴリズム (Detection Algorithm)

本システムは、テキストの「不自然さ」を確率的に評価することでバックドアを検出します。

- **ベースモデル**: GPT-2
- **評価指標**: **PPL (Perplexity; 困惑度)**
- **ロジック**: テキストの交差エントロピー（Cross-Entropy）を計算し、PPLとして数値化します。バックドア（特に無意味型や不可視型）が仕込まれたテキストは、言語モデルにとって「予測しにくい不自然な文字列」となるため、PPLが急上昇する特性を利用して検知します。

---

## 📊 実験結果 (Experimental Results)

自作の評価データセットを用いて検出精度の検証を行いました。

### データセット内訳
- **正常なプロンプト**: 670件
- **バックドア付きプロンプト**: 各種類 10件ずつ

### 検出性能
- 🟢 **検出可能**: 「不可視型（ゼロ幅文字）」および「無意味型」のバックドア
- 🔴 **検出困難**: 「自然言語型」のバックドア

---

## 🚀 今後の課題 (Future Challenges)

- **自然言語型バックドアの検出精度の向上**
  - 文脈に自然に合う単語が使われている場合、GPT-2が計算するPPL（困惑度）が低くなってしまい、正常な文章との区別が難しいという課題があります。今後は、PPL単体ではなく、コンテキストの矛盾度や他の特徴量を組み合わせた新しい検出ロジックのアプローチを検討しています。

---

## 📝 免責事項 (Disclaimer)
本ツールは研究およびセキュリティ監査の目的で開発されています。悪用目的での使用を禁止します。
This tool is developed for research and security auditing purposes only. Malicious use is strictly prohibited.