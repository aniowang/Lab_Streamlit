import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import streamlit as st
import pandas as pd

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

@st.cache_data(ttl=3600, show_spinner="正在加載資料...",experimental_allow_widgets=True)
def page1():
    st.write('[測試]填寫咖啡喜好後送出，程式接收後顯示紀錄')   
    st.write('時間：',pd.Timestamp.now(tz='Asia/Shanghai'))

    #form可以一次選好條件再更新，不用每次選擇每次更新https://30days.streamlit.app/?challenge=Day22
    with st.form('選擇條件後點擊submmit'):
        # Input widgets
        coffee_bean_val = st.selectbox('Coffee bean', ['Arabica', 'Robusta'])
        coffee_roast_val = st.selectbox('Coffee roast', ['Light', 'Medium', 'Dark'])
        brewing_val = st.selectbox('Brewing method', ['Aeropress', 'Drip', 'French press', 'Moka pot', 'Siphon'])
        serving_type_val = st.selectbox('Serving format', ['Hot', 'Iced', 'Frappe'])
        milk_val = st.select_slider('Milk intensity', ['None', 'Low', 'Medium', 'High'])
        owncup_val = st.checkbox('Bring own cup')
    
        # Every form must have a submit button
        submitted = st.form_submit_button('Submit')
    if submitted:
        # st.toast('確認送出囉!')
        st.write('Coffee bean：',coffee_bean_val)
        st.write('Coffee roast：',coffee_roast_val)
        st.write('Brewing method：',brewing_val)
        st.write('Serving format：',serving_type_val)
        st.write('Milk intensity：',milk_val)
        st.write('Bring own cup：',owncup_val)
        cancel_input=st.button('刪除')
        if cancel_input:
            submited=None
    
    #添加側邊攔
    st.sidebar.write('測試版本：V0.0.1') 
    st.sidebar.write('測試時間：',pd.Timestamp.now(tz='Asia/Shanghai')) 
    
if __name__=="__main__":
    if st.session_state["authentication_status"] is None:
        """
        此為測試登入功能以及各頁面檢視權限管控之實驗頁面
    
        請先登入後方可分頁檢視
        """
    #修改登入介面文字
    authenticator.login( 
        location='main',
        fields={'Form name':'登入', 'Username':'使用者名稱', 'Password':'密碼', 'Login':'確認登入'})    
    if st.session_state["authentication_status"]:
        authenticator.logout(location='sidebar',button_name='確認登出')
        st.sidebar.write(f'Welcome *{st.session_state["name"]}*')
        #登入成功後才執行page1()
        
        page1()         
    elif st.session_state["authentication_status"] is False:
        st.error('您輸入的帳號/密碼 錯誤')
    elif st.session_state["authentication_status"] is None:
        st.warning('請輸入您的帳號及密碼')
