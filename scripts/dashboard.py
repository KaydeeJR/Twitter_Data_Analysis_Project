import streamlit as st

class DashboardSetup:
    """
    TODO:
    A class for configuring and customizing a Streamlit dashboard application.


    """
    def __init__(self):
        # web page page configuration
        st.set_page_config(page_title="Twitter Data Analysis", layout="wide")
        
        st.title("Data Display")
        st.markdown("<p style='padding:10px; background-color:#000000;color:#00ECB9;font-size:16px;border-radius:10px;'>Section Break</p>", unsafe_allow_html=True)
        st.title("Data Visualizations")
        
        with st.beta_expander("Show More Graphs"):
            stBarChart()
            langPie()


    def selectHashTag():
        df = loadData()
        hashTags = st.multiselect("choose combaniation of hashtags", list(df['hashtags'].unique()))
        if hashTags:
            df = df[np.isin(df, hashTags).any(axis=1)]
            st.write(df)
    
    def selectLocAndAuth():
        df = loadData()
        location = st.multiselect("choose Location of tweets", list(df['place_coordinate'].unique()))
        lang = st.multiselect("choose Language of tweets", list(df['language'].unique()))

        if location and not lang:
            df = df[np.isin(df, location).any(axis=1)]
            st.write(df)
        elif lang and not location:
            df = df[np.isin(df, lang).any(axis=1)]
            st.write(df)
        elif lang and location:
            location.extend(lang)
            df = df[np.isin(df, location).any(axis=1)]
            st.write(df)
        else:
            st.write(df)
    
    def barChart(data, title, X, Y):
        title = title.title()
        st.title(f'{title} Chart')
        msgChart = (alt.Chart(data).mark_bar().encode(alt.X(f"{X}:N", sort=alt.EncodingSortField(field=f"{Y}", op="values",
                    order='ascending')), y=f"{Y}:Q"))
        st.altair_chart(msgChart, use_container_width=True)
    
    def stBarChart():
        df = loadData()
        dfCount = pd.DataFrame({'Tweet_count': df.groupby(['original_author'])['clean_text'].count()}).reset_index()
        dfCount["original_author"] = dfCount["original_author"].astype(str)
        dfCount = dfCount.sort_values("Tweet_count", ascending=False)

        num = st.slider("Select number of Rankings", 0, 50, 5)
        title = f"Top {num} Ranking By Number of tweets"
        barChart(dfCount.head(num), title, "original_author", "Tweet_count")


    def langPie():
        df = loadData()
        dfLangCount = pd.DataFrame({'Tweet_count': df.groupby(['language'])['clean_text'].count()}).reset_index()
        dfLangCount["language"] = dfLangCount["language"].astype(str)
        dfLangCount = dfLangCount.sort_values("Tweet_count", ascending=False)
        dfLangCount.loc[dfLangCount['Tweet_count'] < 10, 'lang'] = 'Other languages'
        st.title(" Tweets Language pie chart")
        fig = px.pie(dfLangCount, values='Tweet_count', names='language', width=500, height=350)
        fig.update_traces(textposition='inside', textinfo='percent+label')

        colB1, colB2 = st.beta_columns([2.5, 1])

        with colB1:
            st.plotly_chart(fig)
        with colB2:
            st.write(dfLangCount)

if __name__ == "__main__":
    selectHashTag()
    selectLocAndAuth()
