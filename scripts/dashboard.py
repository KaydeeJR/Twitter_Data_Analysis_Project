import streamlit as st
import pandas as pd

class DashboardSetup:
    """
    TODO: documentation
    A class for configuring and customizing a dashboard application built using Streamlit.

    
    """
    def __init__(self, data_file_path):
        # web page default configuration
        st.set_page_config(page_title="Twitter Data Analysis", page_icon=":bird",
        initial_sidebar_state="auto", layout="wide",
        menu_items={
        'About': "# This is a header. This is an *extremely* cool app!",
        'Get Help': 'https://github.com/KaydeeJR/Twitter_Data_Analysis_Project/tree/main'
        })
        # section title
        st.title("Twitter Data Visualizations", help="Visualizations")
        # data to display in the dashboard
        tweets_df = pd.read_json(data_file_path, lines=True)
        # sidebar setup
        self.set_up_tabs(tweets_df)
    

    def set_up_tabs(self, df):
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Data","Created At", "Mentions", "Topic Modelling","Sentiment Analysis"])
        
        with tab1:
            # Show data
            st.header("Data")
            st.dataframe(df)
        
        with tab2:
            # Show line chart
            st.header("Created At")
            st.bar_chart(data=df, x="created_at", y="id", color=None, width=0, height=0, use_container_width=True)

        with tab3:
            # Show bar chart
            st.header("Mentions")
            
        with tab4:
            # Show topic visualization
            st.header("Topic Modelling")
            
        with tab5:
            # Created At - show line chart
            st.header("Sentiment Analysis")
        

    def selectHashTag(self):
        pass
        # df = loadData()
        # hashTags = st.multiselect("choose combaniation of hashtags", list(df['hashtags'].unique()))
        # if hashTags:
        #     df = df[np.isin(df, hashTags).any(axis=1)]
        #     st.write(df)
    
    def selectLocAndAuth(self):
        pass
        # df = loadData()
        # location = st.multiselect("choose Location of tweets", list(df['place_coordinate'].unique()))
        # lang = st.multiselect("choose Language of tweets", list(df['language'].unique()))

        # if location and not lang:
        #     df = df[np.isin(df, location).any(axis=1)]
        #     st.write(df)
        # elif lang and not location:
        #     df = df[np.isin(df, lang).any(axis=1)]
        #     st.write(df)
        # elif lang and location:
        #     location.extend(lang)
        #     df = df[np.isin(df, location).any(axis=1)]
        #     st.write(df)
        # else:
        #     st.write(df)
    
    def barChart(self,data, title, X, Y):
        title = title.title()
        st.title(f'{title} Chart')
        msgChart = (alt.Chart(data).mark_bar().encode(alt.X(f"{X}:N", sort=alt.EncodingSortField(field=f"{Y}", op="values",
                    order='ascending')), y=f"{Y}:Q"))
        st.altair_chart(msgChart, use_container_width=True)
    
    def stBarChart(self):
        pass
        # df = loadData()
        # dfCount = pd.DataFrame({'Tweet_count': df.groupby(['original_author'])['clean_text'].count()}).reset_index()
        # dfCount["original_author"] = dfCount["original_author"].astype(str)
        # dfCount = dfCount.sort_values("Tweet_count", ascending=False)

        # num = st.slider("Select number of Rankings", 0, 50, 5)
        # title = f"Top {num} Ranking By Number of tweets"
        # barChart(dfCount.head(num), title, "original_author", "Tweet_count")


    def langPie(self):
        pass
        # df = loadData()
        # dfLangCount = pd.DataFrame({'Tweet_count': df.groupby(['language'])['clean_text'].count()}).reset_index()
        # dfLangCount["language"] = dfLangCount["language"].astype(str)
        # dfLangCount = dfLangCount.sort_values("Tweet_count", ascending=False)
        # dfLangCount.loc[dfLangCount['Tweet_count'] < 10, 'lang'] = 'Other languages'
        # st.title(" Tweets Language pie chart")
        # fig = px.pie(dfLangCount, values='Tweet_count', names='language', width=500, height=350)
        # fig.update_traces(textposition='inside', textinfo='percent+label')

        # colB1, colB2 = st.beta_columns([2.5, 1])

        # with colB1:
        #     st.plotly_chart(fig)
        # with colB2:
        #     st.write(dfLangCount)

if __name__ == "__main__":
    dashboard = DashboardSetup(r"C:\Users\LENOVO\personal_repos\Twitter_Data_Analysis_Project\data\global_twitter_data.json")
    dashboard.selectHashTag()
    dashboard.selectLocAndAuth()
