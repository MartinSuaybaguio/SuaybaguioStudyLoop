import streamlit as st


class Theme:
    CSS = """
<style>
[data-testid=stSidebar]{min-width:270px}
[data-testid=stSidebar] [role=radiogroup]{gap:10px}
[data-testid=stSidebar] [role=radiogroup] label{width:100%;padding:14px 18px;border-radius:12px;background:#FFFFFF;border:1px solid #D6E6FF;cursor:pointer}
[data-testid=stSidebar] [role=radiogroup] label>div:first-child{display:none}
[data-testid=stSidebar] [role=radiogroup] label p{font-size:1.1rem;font-weight:600}
[data-testid=stSidebar] [role=radiogroup] label:hover{background:#E6F0FF}
[data-testid=stSidebar] [role=radiogroup] label:has(input:checked){background:#1E6FEB;border-color:#1E6FEB}
[data-testid=stSidebar] [role=radiogroup] label:has(input:checked) p{color:#FFFFFF}
[data-testid=stSidebar] .stButton>button{width:100%;padding:.7rem 1rem;font-size:1.05rem}
.stApp, [data-testid=stAppViewContainer], [data-testid=stMain]{background:#FFFFFF;color:#0B2A5B}
[data-testid=stHeader]{background:#FFFFFF;border-bottom:1px solid #E6F0FF}
[data-testid=stHeader] *{color:#0B2A5B}
[data-testid=stAppDeployButton]{display:none}
.block-container{max-width:960px;padding-top:2.5rem}
[data-testid=stSidebar]{background:#F3F8FF;border-right:1px solid #D6E6FF}
.stApp :is(p,span,label,li,small,h1,h2,h3,h4,h5,h6){color:#0B2A5B}
.stApp h1{font-weight:700;letter-spacing:-0.5px}
.stApp h2,.stApp h3{font-weight:600}
[data-testid=stMetricLabel] *,[data-testid=stMetricValue] *{color:#0B2A5B}
[data-testid=stCaptionContainer] *{color:#5B6F94}
.stApp .stButton>button,.stApp .stFormSubmitButton>button{background:#1E6FEB;border:0;border-radius:10px;font-weight:600;padding:.4rem 1.1rem}
.stApp .stButton>button p,.stApp .stFormSubmitButton>button p{color:#FFFFFF}
.stApp .stButton>button:hover,.stApp .stFormSubmitButton>button:hover{background:#1558BF}
.stButton>button:focus-visible{outline:2px solid #0B3D91;outline-offset:2px}
.stApp input,.stApp textarea{background:#FFFFFF!important;color:#0B2A5B!important}
[data-baseweb=input],[data-baseweb=textarea],[data-baseweb=select]>div{background:#FFFFFF!important;border-color:#BBD3F7!important;border-radius:10px!important}
[data-baseweb=popover],[data-baseweb=popover] ul,[data-baseweb=menu]{background:#FFFFFF!important}
[data-baseweb=popover] li,[data-baseweb=calendar] *{color:#0B2A5B}
[data-testid=stExpander]{border:1px solid #D6E6FF;border-radius:12px;background:#FFFFFF}
[data-baseweb=tab-highlight]{background:#1E6FEB}
[data-testid=stMetric]{background:#F3F8FF;border:1px solid #D6E6FF;border-radius:14px;padding:14px 18px}
[data-testid=stVerticalBlockBorderWrapper]{border-color:#D6E6FF!important;border-left:4px solid #1E6FEB!important;border-radius:12px;background:#FFFFFF}
[data-testid=stProgress] div[role=progressbar]>div{background:#1E6FEB}
.stApp .sl-tag{display:inline-block;background:#E6F0FF;color:#1558BF;border-radius:999px;padding:2px 10px;margin-right:6px;font-size:.8rem;font-weight:600}
.stApp .sl-tag.hot{background:#1E6FEB;color:#FFFFFF}
.sl-badge{border:1px solid #1E6FEB;background:#E6F0FF;color:#0B2A5B;border-radius:12px;padding:12px 16px;margin-bottom:10px}
.sl-badge.locked{border-color:#D5DAE3;background:#F5F6F8;color:#8A93A5}
.sl-badge b{display:block;font-size:1rem}
</style>
"""

    @classmethod
    def apply(cls) -> None:
        st.markdown(cls.CSS, unsafe_allow_html=True)
