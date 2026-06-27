import pandas as pd
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from tqdm import tqdm

class P0OnlyPPL:
    def __init__(self, model_name='gpt2'):
        print("モデルロード中")
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        self.model.eval()
        self.tokenizer.pad_token = self.tokenizer.eos_token

        self.attack_order = [
            ('X', 'apple：自然なバックドア'),
            ('Y', 'ゼロ幅文字：不可視トリガー'),
            ('Z', '[TRIGGER]：明示的バックドア')
        ]
        
    def get_ppl(self, text):
        if not isinstance(text, str) or not text.strip():
            return 1e6
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True)
        with torch.no_grad():
            outputs = self.model(**inputs, labels=inputs['input_ids'])
            return torch.exp(outputs.loss).item()
    
    def run(self, csv_path):
        df = pd.read_csv(csv_path)
        print(f"P0分析開始: {csv_path}")
        tqdm.pandas()

        df['ppl'] = df['input'].progress_apply(self.get_ppl)

        print("\n=== 平均PPL（攻撃タイプ別） ===")

        attack_labels = []

        for label, desc in self.attack_order:
            subset = df[df['output'] == label]
            if len(subset) == 0:
                continue
            avg_ppl = subset['ppl'].mean()
            attack_labels.append(label)
            print(f"PPL={avg_ppl:.1f} ({desc})")

        clean_subset = df[~df['output'].isin(attack_labels)]
        if len(clean_subset) > 0:
            clean_ppl = clean_subset['ppl'].mean()
            print(f"PPL={clean_ppl:.1f} (クリーンなデータ)")

        df.to_csv("p0_only_ppl.csv", index=False)
        print("\n結果保存: p0_only_ppl.csv")

# 実行
detector = P0OnlyPPL()
detector.run('backdoor_analysis_data.csv')