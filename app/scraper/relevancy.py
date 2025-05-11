from functools import lru_cache
import numpy as np
from ollama import Client
import unicodedata
import re

client = Client()

LLM_MODEL = "llama3"
EMBED_MODEL = "bge-m3"

@lru_cache(maxsize=None)
def _reference_embs():
    topics = [
        "Romania politics", "Romanian economy", "Romania geopolitics",
        "Bucharest government", "Romanian elections"
    ]
    return [client.embeddings(model=EMBED_MODEL, prompt=t)["embedding"] for t in topics]

def _cosine(a, b):
    a, b = np.asarray(a), np.asarray(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12))

def is_relevant_title(title: str, threshold: float = 0.45) -> bool:
    """
    Uses Ollama LLM to determine if a title is relevant to Romanian politics/economy.
    Falls back to heuristics and embeddings if LLM fails.
    """
    # 1) LLM RELEVANCY CHECK (primary path)
    try:
        prompt = f"""
        Determine if this news headline is relevant to Romanian politics or economy:
        "{title}"
        
        Answer with only one word: "yes", "maybe", or "no".
        """
        
        response = client.generate(model=LLM_MODEL, prompt=prompt)
        answer = response['response'].strip().lower()
        
        if "yes" in answer:
            return True
        if "no" in answer:
            return False
        # For "maybe" or unclear responses, continue to fallback methods
    except Exception as e:
        print(f"LLM relevancy check failed for {title=}: {e}")
        # Continue to fallback methods
    
    # 2) RULE MATCHES (fallback)
    text = normalize(title)
    has_ro = any(p.search(text) for p in ROMANIAN_PATTERNS)
    has_topic = any(p.search(text) for p in POL_ECON_PATTERNS)
    if has_ro and has_topic:
        return True

    # 3) EMBEDDING SIMILARITY (final fallback)
    try:
        emb = client.embeddings(model=EMBED_MODEL, prompt=title)["embedding"]
        sims = (_cosine(emb, ref) for ref in _reference_embs())
        if max(sims) >= threshold:
            return True
    except Exception as e:
        print(f"Error embedding {title=}: {e}")
        pass

    return False

_WHITESPACE_RE = re.compile(r"\s+")

def normalize(text: str) -> str:
    # NFC → canonical form, strip diacritics, lowercase, collapse spaces
    text = unicodedata.normalize("NFC", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower()
    return _WHITESPACE_RE.sub(" ", text).strip()

ROMANIAN_PATTERNS = [
    re.compile(p) for p in [
        r"\bromania\b", r"\broman(?:a|e|i|ilor|esc\w*)\b",
        r"\bbucurest\w*\b", r"\bbucharest\b",
    ]
]

POL_ECON_PATTERNS = [
    re.compile(p) for p in [
        r"\bguvern\w*\b", r"\bminister\w*\b", r"\bparlament\w*\b",
        r"\baleger\w*\b", r"\bpolitic\w*\b", r"\bpartid\w*\b",
        r"\bpresedint\w*\b", r"\bpremier\b", r"\bprim[- ]?ministr\w*\b",
        r"\bbuget\w*\b", r"\bfiscal\w*\b", r"\beconomic\w*\b",
        r"\binflati\w*\b", r"\bgeopolitic\w*\b",    #  NEW: covers "geopolitica"
    ]
]
