from langgraph.graph import StateGraph, END
from state.bi_state import BIState
from node.to_sql import to_sql_node
from node.run_sql import run_sql_node
from node.viz import viz_node

def build_graph(llm, db, engine):
    g = StateGraph(BIState)
    g.add_node("to_sql", lambda s: to_sql_node(s, llm, db))
    g.add_node("run_sql", lambda s: run_sql_node(s, engine))
    g.add_node("make_viz", viz_node)
    g.set_entry_point("to_sql")
    g.add_edge("to_sql", "run_sql")
    g.add_edge("run_sql", "make_viz")
    g.add_edge("make_viz", END)
    return g.compile()