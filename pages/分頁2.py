import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import streamlit as st
import pandas as pd
import numpy as np

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

@st.cache_data(experimental_allow_widgets=True)  # 👈 Add the caching decorator
def load_data(url):
    df = pd.read_csv(url)
    return df
    

def page2():    
    st.write('測試時間：',pd.Timestamp.now(tz='Asia/Shanghai'))
    
    #添加側邊攔
    st.sidebar.write('測試版本：V0.0.1') 
    st.sidebar.write('測試時間：',pd.Timestamp.now(tz='Asia/Shanghai')) 
    n = None
    
    df = load_data("https://github.com/plotly/datasets/raw/master/uber-rides-data1.csv")
      
    n=np.random.randint(1,20)
    st.write('隨機顯示行數：',n)
    st.dataframe(df.head(n))
    #點擊按鈕後刷新頁面
    if st.button("Rerun"):
        st..experimental_rerun()
    #st.toast('頁面已更新')


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
        page2()         
    elif st.session_state["authentication_status"] is False:
        st.error('您輸入的帳號/密碼 錯誤')
    elif st.session_state["authentication_status"] is None:
        st.warning('請輸入您的帳號及密碼')
