# ============================================
# FILE: utils/helpers.py
# ============================================
"""Helper utility functions"""
import os
from typing import Optional

def ensure_dir_exists(directory: str):
    """Create directory if it doesn't exist"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def validate_api_key(api_key: Optional[str]) -> bool:
    """Validate API key format"""
    if not api_key:
        return False
    return len(api_key) > 20

