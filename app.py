import streamlit as st
import altair as alt
from llm.groq_client import get_llm
from database.sql import get_engine, get_db
from graph.bi_graph import build_graph
from state.bi_state import BIState

st.set_page_config(page_title="BI Agent", page_icon="📊", layout="wide")

def init():
    return build_graph(get_llm(), get_db(get_engine()), get_engine())

graph = init()
st.title("📊 CHAT-BI")
q = st.text_input("Ask about your data", "students with grade A")
run = st.button("Run")

if run and q:
    with st.spinner("Processing..."):
        result = graph.invoke(BIState(user_query=q, sql=None, df=None, viz=None, error=None))
        
        if result.get("error"):
            st.error(result["error"])
        if result.get("sql"):
            st.code(result["sql"], language="sql")
        if result.get("df") is not None:
            st.dataframe(result["df"], use_container_width=True)
        
        viz = result.get("viz")
        if viz and result.get("df") is not None and not result["df"].empty:
            df = result["df"]
            if viz["type"] == "bar":
                st.altair_chart(alt.Chart(df).mark_bar().encode(x=viz["x"], y=viz["y"]), use_container_width=True)
            elif viz["type"] == "scatter":
                st.altair_chart(alt.Chart(df).mark_circle().encode(x=viz["x"], y=viz["y"]), use_container_width=True)

