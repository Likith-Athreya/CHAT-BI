import pandas as pd
from state.bi_state import BIState

def viz_node(state: BIState) -> BIState:
    df = state.get("df")
    if df is None or df.empty:
        return state
    
    nums = df.select_dtypes(include=["number"]).columns.tolist()
    cats = df.select_dtypes(include=["object", "category"]).columns.tolist()
    
    if nums and cats:
        state["viz"] = {"type": "bar", "x": cats[0], "y": nums[0]}
    elif len(nums) >= 2:
        state["viz"] = {"type": "scatter", "x": nums[0], "y": nums[1]}
    else:
        state["viz"] = {"type": "table"}
    
    return state

