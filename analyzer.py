import os
import logging

# 1. SILENCE PROTOCOL: Must happen BEFORE importing torch or transformers
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# Mute the specific logger that prints the "Unexpected Key" report
logging.getLogger("transformers.modeling_utils").setLevel(logging.ERROR)
logging.getLogger("transformers.configuration_utils").setLevel(logging.ERROR)

import torch
from transformers import (
    BertTokenizer,
    BertForSequenceClassification,
    pipeline,
    Pipeline,
    logging as transformers_logging,
)
from typing import Any, cast

# Mute the high-level transformers library logs
transformers_logging.set_verbosity_error()


class SentimentAnalyzer:
    def __init__(self):
        self.model_name = "ProsusAI/finbert"

        # Arch/CPU Optimization
        torch.set_num_threads(torch.get_num_threads())

        # Initializing models silently
        self.tokenizer = BertTokenizer.from_pretrained(self.model_name, verbose=False)
        self.model = BertForSequenceClassification.from_pretrained(self.model_name)

        # Bypassing the 'no overloads' LSP error
        pipe_factory: Any = pipeline
        self.nlp = cast(
            Pipeline,
            pipe_factory(
                task="sentiment-analysis",
                model=self.model,
                tokenizer=self.tokenizer,
                device=-1,
            ),
        )

        self.model.eval()
        self.final_vibe = 0.0

    def analyze_headlines(self, headlines: list[str]) -> list[dict[str, Any]]:
        if not headlines:
            self.final_vibe = 0.0
            return []

        with torch.inference_mode():
            results = self.nlp(headlines)

        processed_results = []
        active_signals = []
        score_map = {"positive": 1.0, "neutral": 0.0, "negative": -1.0}

        for i, res in enumerate(results):
            label = res["label"].lower()
            confidence = res["score"]

            if confidence > 0.85:
                base_score = score_map.get(label, 0.0)
            else:
                base_score = 0.0

            if base_score < 0:
                weighted_score = base_score * 1.5
            else:
                weighted_score = base_score

            if weighted_score != 0:
                active_signals.append(weighted_score)

            processed_results.append(
                {
                    "headline": headlines[i],
                    "sentiment": label,
                    "confidence": round(confidence, 4),
                    "score_val": weighted_score,
                }
            )

        if active_signals:
            raw_vibe = sum(active_signals) / len(active_signals)
            self.final_vibe = max(min(raw_vibe, 1.0), -1.0)
        else:
            self.final_vibe = 0.0

        return processed_results
