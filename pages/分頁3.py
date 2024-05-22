import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import plotly.express as px

"""
    測試讀取Chinook (sqlite)  
    (資料來源：SQLite Tutorial ) https://www.sqlitetutorial.net/sqlite-sample-database/
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

    select * from tracks;
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

    # st.write("專輯資訊",table_albums[table_albums['Title']==Albums_title])

    #根據選擇，顯示專輯作者
    if Albums_title:
        ArtistId=table_albums[table_albums['Title']==Albums_title]['ArtistId']
        
        # st.success(fr"您選擇的專輯是：{Albums_title}")

        sql=f"""
        select Name from artists
        where  ArtistId = {int(ArtistId[0])}
        ;
        """
        Artist=pd.read_sql(sql,conn)
        st.write("專輯作者是：",Artist["Name"][0])

    #根據選擇，顯示歌曲清單
    if Albums_title:
        AlbumId=table_albums[table_albums['Title']==Albums_title]['AlbumId']
        
        # st.success(f"專輯歌曲有：{Albums_title}")
        sql=f"""
        select a.Name ,b.Name as Format,c.Name as MusicType from tracks a
        left join (select * from media_types) b on b.MediaTypeId=a.MediaTypeId
        left join (select * from genres) c on c.GenreId=a.GenreId
        where  a.AlbumId = {int(AlbumId[0])}
        ;
        """
        Artist=pd.read_sql(sql,conn)
        st.write("專輯歌曲有：",Artist)

        #選擇單曲
        Song=st.selectbox("選擇想檢視的單曲名稱",Artist['Name'])

        sql="""
        select Name,TrackId from tracks
        """
        SongList=pd.read_sql(sql,conn)

        SongId=SongList[SongList["Name"]==Song].reset_index(drop=True)['TrackId'][0]

        # st.write(SongId)
        # st.write(Song)
        if Song:
            sql=fr"""
                select a.*,b.InvoiceLineId,b.Quantity,c.* from invoices a
                left join (select * from invoice_items) b on a.invoiceId = b.invoiceId
                left join (select * from tracks) c on c.TrackId = b.TrackId
                where c.TrackId ={SongId}
                order by a.InvoiceId desc 
                """
            Song_txn=pd.read_sql(sql,conn)
            if Song_txn.shape[0]>0:
                st.write("單曲銷售紀錄：",Song_txn)
            else:
                st.warning("無銷售紀錄")

    #根據選擇顯示專輯銷售金額
    sql=f"""
    select a.*,b.InvoiceLineId,b.Quantity,c.* from invoices a
    left join (select * from invoice_items) b on a.invoiceId = b.invoiceId
    left join (select * from tracks) c on c.TrackId = b.TrackId
    where c.AlbumId = {int(AlbumId[0])}
    order by a.InvoiceId desc ;
    """
    Txn=pd.read_sql(sql,conn)

    if Txn.shape[0]>0:
        st.write("專輯相關銷售紀錄：",Txn)
    else:
        st.warning("無專輯銷售紀錄")

    # col1,col2 = st.columns(2)

    # with col1:
    fig=px.bar(Txn,x="Name",y="Total")
    st.plotly_chart(fig,use_container_width=True,height=200)
    
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
