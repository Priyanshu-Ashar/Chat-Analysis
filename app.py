import streamlit as st
import matplotlib.pyplot as plt
import preprocessor, helper

import seaborn as sns

st.title("CHAT ANALYSIS")
st.sidebar.title("CHAT SENTIMENT ANALYSIS")

uploded_file = st.sidebar.file_uploader("Choose a file")
if uploded_file is not None:
    bytes_data = uploded_file.getvalue()
    data = bytes_data.decode("utf-8")
    
    # st.text(data)
    df = preprocessor.preprocess(data)
    st.dataframe(df)

    user_list = df['user'].unique().tolist()
    user_list.remove('Group Notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show Analysis w.r.t", user_list)
      
    if st.sidebar.button("Show Analysis"):
        st.title('TOP STATS')
        num_messages , words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        
        with col2:
            st.header("Total Words")
            st.title(words)
        
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        
        with col4:
            st.header("Links Shared")
            st.title(num_links)
        
        # FINDING THE BUSIEST USER IN THE GROUP:-
        
        if selected_user == 'Overall':
            st.title("Most Busy User")
            x = helper.most_busy_user(df)
            x1 = helper.most_busy_user_pie(df)
            
            fig,ax = plt.subplots()
            

            col1, col2 = st.columns(2)

            with col1:
                
                ax.bar(x.index, x.values, color = 'orange', edgecolor = 'black')
                # ax.set_facecolor('black')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with col2:
                patches, texts, pcts = ax.pie(x1.values , labels = x1.index,wedgeprops={'linewidth' : 3.0, 'edgecolor' : 'white'}, textprops= {'size': 'x-large'},  autopct = '%1.1f%%', radius = 1.8)
                for i, patch in enumerate(patches):
                    texts[i].set_color(patch.get_facecolor())
                    plt.setp(pcts, color = 'white')
                    plt.setp(texts, fontweight = 500)

                
                st.pyplot(fig)
        
        
        # MONTHLY TIMELINE:-
        st.title('MONTHLY TIMELINE')
        timeline = helper.monthly_timeline(selected_user, df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color = 'orange')
        plt.xticks(rotation = 'vertical')
        plt.grid(True)
        st.pyplot(fig)

        # ACTIVITY MAP:-
        st.title('ACTIVITY MAP')
        col1, col2 = st.columns(2)        
        with col1:
            st.header("MOST BUSY DAY")
            busy_day = helper.weekly_activity(selected_user, df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color = 'orange', edgecolor = 'black')
            # ax.set_facecolor('black')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)
        
        with col2:
            st.header("MOST BUSY MONTH")
            busy_month = helper.monthly_activity(selected_user, df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color = 'orange', edgecolor = 'black')
            # ax.set_facecolor('black')
            plt.xticks(rotation = 'vertical')
            
            st.pyplot(fig)
        
        st.title("Activity Heatmap")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
        

            
            
