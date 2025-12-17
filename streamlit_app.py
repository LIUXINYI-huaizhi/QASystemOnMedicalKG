import streamlit as st
from py2neo import Graph

st.set_page_config(page_title="医疗知识图谱问答系统", layout="centered")

st.title("🩺 医疗知识图谱问答系统")

st.write("基于 Neo4j 医疗知识图谱的智能问答演示系统")

# ========= 连接 Neo4j（远程服务器） =========
# ⚠️ 这里先写死，后面会教你改成 secrets
NEO4J_URL = "http://你的服务器IP:7474"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "project"

graph = Graph(
    NEO4J_URL,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)

# ========= 输入问题 =========
question = st.text_input(
    "请输入你的问题：",
    placeholder="例如：感冒有什么症状？"
)

# ========= 简单示例问答逻辑 =========
if question:
    if "症状" in question:
        disease = question.replace("有什么症状", "").replace("有哪些症状", "")
        cypher = """
        MATCH (d:Disease {name:$name})-[:HAS_SYMPTOM]->(s)
        RETURN s.name
        """
        result = graph.run(cypher, name=disease).data()

        if result:
            st.success(f"【{disease}】的症状包括：")
            for r in result:
                st.write("•", r["s.name"])
        else:
            st.warning("未查询到相关疾病或症状信息。")

    else:
        st.info("当前示例仅支持“某疾病有什么症状”类问题。")
