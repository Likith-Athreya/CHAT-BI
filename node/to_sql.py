import os
from langchain_community.agent_toolkits import create_sql_agent
from state.bi_state import BIState

def looks_like_sql(text: str) -> bool:
    if not text:
        return False
    t = text.strip().lower()
    return (t.startswith("select") or t.startswith("with") or any(k in t for k in ["insert", "update", "delete", "create", "drop", "alter"]))


def clean_sql(raw: str) -> str:
    if not raw:
        return raw
    s = raw.strip()

    if '"query":' in s:
        try:
            start = s.find('"query":')
            start = s.find('"', start + 8) + 1
            end = s.find('"', start)
            if start > 0 and end > start:
                cand = s[start:end]
                return cand.strip()
        except Exception:
            pass

    if "```" in s:
        parts = s.split("```")
        if len(parts) >= 2:
            inner = parts[1].strip()
            if inner.lower().startswith("sql\n"):
                inner = inner[4:]
            s = inner.strip()
    s = s.replace("= null", "IS NULL").replace("= NULL", "IS NULL")
    return s.replace("`", "").strip()


def fallback_generate_sql(llm, db, question: str) -> str:
    try:
        schema = db.get_table_info()
    except Exception:
        schema = ""
    prompt = (
        "You are a PostgreSQL expert. Using the schema below, write ONE valid SQL query "
    "that answers the user's request. The query may be SELECT, INSERT, UPDATE, or DELETE "
    "depending on the question. Return ONLY the SQL.\n\n"
    "⚠️ Important rules: Use IS NULL / IS NOT NULL instead of = NULL. Always include a WHERE clause for UPDATE or DELETE.\n\n"
    f"Schema:\n{schema}\n\nQuestion: {question}\n"
    )
    resp = llm.invoke(prompt)
    return clean_sql(getattr(resp, "content", str(resp)))


def extract_sql_from_agent_output(out) -> str | None:
    raw = out.get("output") if isinstance(out, dict) else str(out)
    sql = clean_sql(raw) if raw else None
    if sql and looks_like_sql(sql):
        return sql

    steps = out.get("intermediate_steps") if isinstance(out, dict) else None
    if isinstance(steps, list):
        for step in steps:
            if not (isinstance(step, tuple) and len(step) >= 2):
                continue
            action, observation = step
            tool_input = getattr(action, "tool_input", None)
            if isinstance(tool_input, dict) and "query" in tool_input:
                cand = str(tool_input["query"]).strip()
                if looks_like_sql(cand):
                    return cand
            if isinstance(tool_input, str) and looks_like_sql(tool_input):
                return tool_input.strip()
            if isinstance(observation, str) and looks_like_sql(observation):
                return observation.strip()
    return None


def to_sql_node(state: BIState, llm, db) -> BIState:
    question = state["user_query"]

    if os.getenv("SQL_ONLY_MODE", "False").lower() == "true":
        sql = fallback_generate_sql(llm, db, question)
        state["sql"] = sql if looks_like_sql(sql) else None
        if not state["sql"]:
            state["error"] = "Could not generate valid SQL. Please try rephrasing."
        return state

    agent = create_sql_agent(llm=llm, db=db, agent_type="openai-tools", verbose=False)
    out = agent.invoke({"input": question})
    sql = extract_sql_from_agent_output(out)
    if not sql:
        sql = fallback_generate_sql(llm, db, question)
    state["sql"] = sql if looks_like_sql(sql) else None
    if not state["sql"]:
        state["error"] = "Could not generate valid SQL. Please try rephrasing."
    return state

