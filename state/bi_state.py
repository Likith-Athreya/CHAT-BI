from typing import Optional, Dict, Any
import pandas as pd

class BIState(dict):
    user_query: str
    sql: Optional[str]
    df: Optional[pd.DataFrame]
    viz: Optional[Dict[str, Any]]
    error: Optional[str]

