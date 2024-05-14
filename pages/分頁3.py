import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import streamlit as st
import pandas as pd
import numpy as np
import sqlite3

"""

    測試讀取sqlite db

"""


with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

    
# @st.cache_data(experimental_allow_widgets=True)  # 👈 Add the caching decorator
def page3():    

    # st.write('測試時間：',pd.Timestamp.now(tz='Asia/Shanghai'))
    
    #添加側邊攔
    st.sidebar.write('測試版本：V0.0.1') 
    st.sidebar.write('測試時間：',pd.Timestamp.now(tz='Asia/Shanghai')) 
    # n = None
    # n=np.random.randint(1,20)
    # st.write('顯示隨機整數：',n)
    # #點擊按鈕後刷新頁面
    # if st.button("Rerun"):
    #     st.rerun()
    #顯示toml變數
    # st.write("隱藏變數：",st.secrets["test_var1"])

    #測試讀取db
    conn = sqlite3.connect('./sqlite/chinook.db')
    sql="""
    --select * from sqlite_master
    --where type='table';

    select * from artists;
    """    
    table1=pd.read_sql(sql,conn)
    st.write(table1)
    # table1["tbl_name"]

    #測試讀取單一表單
    sql="""
    select * from albums;
    """
    table_albums=pd.read_sql(sql,conn)

    Albums_title_list=list(table_albums["Title"])

    Albums_title=st.selectbox("選擇想檢視的專輯名稱",Albums_title_list)
    
    st.write("專輯ID",table_albums[table_albums['Title']==Albums_title])

    #根據選擇，顯示專輯作者
    if Albums_title:
        ArtistId=table_albums[table_albums['Title']==Albums_title]['ArtistId']
        
        st.success(f"您選擇的專輯是：{Albums_title}")
        sql=f"""
        select Name from artists
        where  ArtistId = {int(ArtistId)}
        ;
        """
        Artist=pd.read_sql(sql,conn)
        st.write("專輯作者是：",Artist["Name"][0])


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
        #登入成功後才執行page3()
        page3()         
    elif st.session_state["authentication_status"] is False:
        st.error('您輸入的帳號/密碼 錯誤')
    elif st.session_state["authentication_status"] is None:
        st.warning('請輸入您的帳號及密碼')
