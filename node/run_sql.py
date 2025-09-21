from state.bi_state import BIState
from database.sql import run_sql

def looks_like_sql(text: str) -> bool:
    if not text:
        return False
    t = str(text).strip().lower()
    return t.startswith(("select", "with")) or any(k in t for k in ("insert", "update", "delete", "create", "drop", "alter"))

def run_sql_node(state: BIState, engine) -> BIState:
    sql = state.get("sql")
    if not sql:
        return state
    if not looks_like_sql(sql):
        state["error"] = "Generated text was not SQL. Please rephrase your question."
        return state
    try:
        state["df"] = run_sql(engine, sql)
    except Exception as e:
        state["error"] = str(e)
    return state

