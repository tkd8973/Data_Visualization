import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objs as go


def heatmap():
    aa=datas.groupby([datas['weekday'],datas['time'],datas['age'],datas['sex']])[['Tag']].value_counts() # 평/주말과 시간,나이,성별에 대한 종목들의 카운트
    aa = pd.DataFrame(aa)
    aa = aa.unstack()
    aa.fillna(0,inplace=True)

    px.imshow(aa)

def Preprocess(df2):    
    df2.columns = ['Year_Month','Tag','weekday','day','time','sex','age','sum']
    df2 = df2[df2['sum']>1000]
    df2.sort_values(by=['age','time'],inplace=True)
    ages = df2.age.unique()

    df2['age']=df2['age'].apply(lambda x:[int(((i+1)*10)+10) for i,v in enumerate(ages) if x==v][0])
    datas = df2[(df2['age']==20) | (df2['age']==30)]

    return datas

def hist_plot(data,x,y):
    fig = px.histogram(datas,x=x,color=y, barmode='group')
    st.plotly_chart(fig)


def prod(YM,tag,sex):
    total=datas.loc[(datas['Year_Month'] == YM) & (datas['sex']==sex)]
    return (total.loc[total['Tag']==tag]['sum'].sum() / total['sum'].sum())*100

def pie():
    YM = np.sort(datas['Year_Month'].unique())
    tags = datas['Tag'].unique()[:9]
    fig = make_subplots(rows=1, cols=6, specs=[[{'type': 'domain'}]*6],
                    subplot_titles=('201905F','201905M','202005F','202005M','202105F','202105M'))
    cnt=1
    Female=[]
    Man=[]

    for i in YM:
        for j in tags:
            Female.append(prod(i,j,'F'))
            Man.append(prod(i,j,'M'))

        pie_data_F =[{'labels': tags, 'values': Female, 'name': str(i)+'F'}]
        pie_data_M =[{'labels': tags, 'values': Man, 'name': str(i)+'M'}]
        
        for k, data in enumerate(pie_data_F):
            fig.add_trace(go.Pie(labels=data['labels'], values=data['values'], name=data['name']), 1, cnt)
        for k, data in enumerate(pie_data_M):
            fig.add_trace(go.Pie(labels=data['labels'], values=data['values'], name=data['name']), 1, cnt+3)
        
        cnt+=1
        Female=[]
        Man=[]
        
    st.plotly_chart(fig)


df = pd.read_excel('C:\\Users\\tkd89\\OneDrive\\바탕 화면\\1758015\\PlayDATA\\mp_visualization\\KDX2021_SSC_ONLINE_DATA.xlsx')
df2 = df.copy()
datas = Preprocess(df2)
tab0, tab1, tab2, tab3 = st.tabs(["🏠 Homepage", "📈 Chart", "🗃 Data", "🖇️ Link"])

with tab0:
    tab0.subheader("💸시간대 별 2030 광고 노출 추천리스트💸")
    st.write()
    '''
    **⬆️위의 탭에 있는 메뉴를 클릭해 선택하신 항목을 볼 수 있습니다!⬆️**
    '''
    st.image("https://cdn.pixabay.com/photo/2018/01/07/20/56/graph-3068300_960_720.jpg", width=400)
    '''
    ---
     ### Team 💪
    | 이름 | 자료 수집 및 추출 | 데이터 시각화 |
    | :---: | :---: | :---: |
    | 서상원 | 각년도의 남녀종목건수에 대한 비율 시간/나이/성별에 대한 plot  | 그래프 시각화 |
    | 김명현 | 년도, 성별(나이포함)에 대한 구매 품목 상위 5개 변화추이 그래프 | Streamlit 작성 |
    | 배진우 | countplot으로 평일/휴일의 상품판매량 대한 그래프  | 그래프 시각화 |
    
    #### 자료 설명
    > * 19,20,21년 5월의 인터넷 쇼핑 데이터를 분석하여 2~30대의 인터넷쇼핑 소비 트렌드를 분석.  
    > * 그에 맞춰 시간대 별 쇼핑 추천 리스트를 노출 하는 것을 목표로 한다.
   
    '''
with tab1:
    tab1.subheader("📈 Chart Tab")
    tab1.write()
    
    option = st.selectbox(
    '원하는 차트유형을 골라주세요',
    ('Bar', 'Pie', 'Heatmap'))
    if option == 'Bar':
        option = st.selectbox(
        '원하는 차트를 골라주세요',
        ('성별에 따른 상품 구매량', '평일/주말에 따른 상품 구매량', '나이에 따른 상품 구매량'))
        if option == '성별에 따른 상품 구매량':
            st.write("성별에 따른 상품구매량")
            hist_plot(datas,'sex','Tag')

        elif option == '평일/주말에 따른 상품 구매량':
            st.write("평일/주말에 따른 상품 구매량")
            hist_plot(datas,'weekday','Tag')

        elif option == '나이에 따른 상품 구매량':
            st.write("평일/주말에 따른 상품 구매량")
            hist_plot(datas,'age','Tag')

    elif option == 'Pie':
        st.write("년도별 성별에 따른 상품 구매량")
        pie()    
    elif option == 'Heatmap':
        st.write("히트맵 인덱스가 날아가네요 자세한건 Colab에서")
         
with tab2:
    tab2.subheader("🗃 Data Tab")
    datas.head()
    tab2.write()

    '''
    ---
    ### 
    * KDX2021_SSC_ONLINE_DATA
    * 온라인쇼핑의 세부 업종별 소비 특징 데이터. '19.5월/'20.5월/'21.5월 기간에 대해 14개의 주요 온라인 쇼핑 업종의 연령/성별/구매시간대별 소비 건수를 집계한 데이터
    > [데이터 다운로드](https://kdx.kr/data/view/31454)
    * 데이터출처 : KDX 한국데이터거래소
    ---
    '''
    
with tab3:
    tab3.subheader("🖇️ Link Tab")
    tab3.write("추가적인 자료는 Google Colab 링크를 첨부해드립니다!")
    st.write()
    '''
    * colab링크
    > [Colab](https://colab.research.google.com/drive/1hqqOwwSKjBi1zvcR3xalsBCklYpjx0vq?usp=sharing)
    * Github링크
    > [Github](https://github.com/tkd8973/Data_Visualization) 
    '''