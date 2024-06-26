# Contents of ~/my_app/streamlit_app.py
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import pandas as pd
import os
import sqlite3

st.set_page_config(layout="wide")

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

def main_page():
    st.markdown("# Main page 🎈")
    st.write('現在時間時區',pd.Timestamp.now(tz='Asia/Shanghai'))
    #添加側邊攔
    st.sidebar.write('測試版本：V0.0.1') 
    st.sidebar.write('測試時間：',pd.Timestamp.now()) 
   
    # try:
    #     sqlite3.connect('ex.db')
    #     st.write('建立db')
    # except:
    #     st.write('未建立db')

    st.write(os.listdir())

    #透過設定可以將變數加密使用 https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management
    #st.write('秘密使用者字串', st.secrets['user_name'])
    

if __name__=="__main__": 
    st.write(st.session_state["authentication_status"])
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
        #登入成功後才執行main()
        main_page() 
        
    elif st.session_state["authentication_status"] is False:
        st.error('您輸入的帳號/密碼 錯誤')
    elif st.session_state["authentication_status"] is None:
        st.warning('請輸入您的帳號及密碼')
