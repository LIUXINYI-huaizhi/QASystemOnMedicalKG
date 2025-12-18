import streamlit as st
from chatbot_graph import ChatBotGraph

# ================= 页面配置 =================
st.set_page_config(
    page_title="Medical 罗伯特｜医疗知识图谱问答系统",
    page_icon="🩺",
    layout="centered"
)

# ================= 侧边栏 =================
with st.sidebar:
    st.title("🩺 Medical 罗伯特")
    st.markdown("""
    **Medical Robert（医疗知识图谱问答系统）**

    - 基于 Neo4j 医疗知识图谱  
    - 采用规则 + AC 自动机进行问题理解  
    - 支持疾病 / 症状 / 药物 / 治疗方式查询  
    - 面向教学与课程设计演示
    """)

    st.markdown("### 💡 示例问题")
    example_questions = [
        "板蓝根颗粒能治啥病？",
        "高血压要怎么治？",
        "感冒有什么症状？",
        "糖尿病吃什么药？"
    ]

    for q in example_questions:
        if st.button(q):
            st.session_state.input_question = q

    st.markdown("---")

    if st.button("🗑️ 清空对话"):
        st.session_state.history = []

    st.markdown(
        "<small style='color:gray;'>"
        "⚠️ 本系统仅用于学习与课程设计演示，不构成医疗建议"
        "</small>",
        unsafe_allow_html=True
    )

# ================= 主页面 =================
st.title("🩺 Medical 罗伯特")
st.caption("基于 Neo4j 医疗知识图谱的智能问答系统")

# ================= 初始化问答系统（只初始化一次） =================
@st.cache_resource
def load_bot():
    return ChatBotGraph()

bot = load_bot()

# ================= 会话状态 =================
if "history" not in st.session_state:
    st.session_state.history = []

if "input_question" not in st.session_state:
    st.session_state.input_question = ""

# ================= 输入区 =================
question = st.text_input(
    "请输入你的问题：",
    value=st.session_state.input_question,
    placeholder="例如：板蓝根颗粒能治啥病？",
    key="input_box"
)

# ================= 提交按钮 =================
if st.button("🚀 发送") and question:
    with st.spinner("Medical 罗伯特正在分析中..."):
        answer = bot.chat_main(question)

    st.session_state.history.append(("user", question))
    st.session_state.history.append(("bot", answer))
    st.session_state.input_question = ""

# ================= 聊天展示 =================
st.markdown("---")

for role, content in st.session_state.history:
    if role == "user":
        st.markdown(
            f"""
            <div style="
                background-color:#e8f0fe;
                padding:12px;
                border-radius:12px;
                margin-bottom:8px;
                ">
            🧑 <b>用户</b><br>
            {content}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style="
                background-color:#f1f3f4;
                padding:12px;
                border-radius:12px;
                margin-bottom:16px;
                ">
            🤖 <b>Medical 罗伯特</b><br>
            {content}
            </div>
            """,
            unsafe_allow_html=True
        )
