import os
import logging
import warnings
import torch
from typing import Any, List, Dict, cast

# 1. TOTAL SILENCE PROTOCOL (Must be at the very top)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"  # Stop download bars
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

warnings.filterwarnings("ignore")
logging.captureWarnings(True)

# Mute specific library loggers
for logger_name in ["transformers", "huggingface_hub", "torch"]:
    logging.getLogger(logger_name).setLevel(logging.ERROR)
from transformers import (
    BertTokenizer,
    BertForSequenceClassification,
    pipeline,
    Pipeline,
    logging as transformers_logging,
)

transformers_logging.set_verbosity_error()


class SentimentAnalyzer:
    def __init__(self):
        self.model_name = "ProsusAI/finbert"

        # Arch/CPU Optimization
        self.device = 0 if torch.cuda.is_available() else -1
        if self.device == -1:
            torch.set_num_threads(torch.get_num_threads())

        # Initializing models with explicit silence
        self.tokenizer = BertTokenizer.from_pretrained(
            self.model_name, local_files_only=False, clean_up_tokenization_spaces=True
        )

        # This specific call usually triggers the 'Weights' text
        # We wrap it to ensure no stderr leakage
        self.model = BertForSequenceClassification.from_pretrained(
            self.model_name, low_cpu_mem_usage=True
        )

        pipe_factory: Any = pipeline
        self.nlp = cast(
            Pipeline,
            pipe_factory(
                task="sentiment-analysis",
                model=self.model,
                tokenizer=self.tokenizer,
                device=self.device,
            ),
        )

        self.model.eval()
        self.final_vibe = 0.0

    def analyze_comprehensive(self, news_items: List[Dict[str, Any]]) -> float:
        """
        Expects a list of dicts: [{'headline': '...', 'type': 'MACRO/TICKER'}]
        Uses weighted importance: Macro news carries more 'weight' than ticker news.
        """
        if not news_items:
            self.final_vibe = 0.0
            return 0.0

        headlines = [item["headline"] for item in news_items]

        with torch.inference_mode():
            # Batch processing for speed
            results = self.nlp(headlines)

        weighted_scores = []
        # Score Mapping
        score_map = {"positive": 1.0, "neutral": 0.0, "negative": -1.0}

        for i, res in enumerate(results):
            label = res["label"].lower()
            confidence = res["score"]
            news_type = news_items[i].get("type", "TICKER")

            # 1. Basic Sentiment Score
            base_score = score_map.get(label, 0.0) * confidence

            # 2. Contextual Weighting Logic
            # Macro news (World events) is 2.5x more important for market direction
            weight = 2.5 if news_type != "TICKER" else 1.0

            # 3. Asymmetric Risk (Negative news is more impactful than positive)
            if base_score < 0:
                weight *= 1.5

            weighted_scores.append(base_score * weight)

        if weighted_scores:
            # We use a moving average style to prevent one headline from ruining the score
            raw_vibe = sum(weighted_scores) / len(weighted_scores)
            # Squash to [-1, 1] range
            self.final_vibe = max(min(raw_vibe, 1.0), -1.0)
        else:
            self.final_vibe = 0.0

        return self.final_vibe
