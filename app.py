import streamlit as st
import base64
import requests
from PIL import Image
import pandas as pd
import re


# Initial page config
st.set_page_config(
    page_title="TidyTuesday",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🎨",

)

class ImagesURL:
    icon = "images/tt_logo.png"
    icon2 = "images/tt_logo2.png"

# Define img_to_bytes() function
def img_to_bytes(img_url):
    response = requests.get(img_url)
    img_bytes = response.content
    encoded = base64.b64encode(img_bytes).decode()
    return encoded



# main function
def main():
    """
    Main function to set up the Streamlit app layout.
    """
    cs_sidebar()
    cs_body()
    return None

# Define the cs_sidebar() function
def cs_sidebar():
    """
    Populate the sidebar with various content sections related to Python.
    """

    image = Image.open(ImagesURL.icon2)
    st.sidebar.image(image)



    st.sidebar.header("TidyTuesday")


    # Sidebar: About TidyTuesday
    with st.sidebar:
        with st.expander("__📊 About TidyTuesday__"):
            st.markdown("""
            - [TidyTuesday](https://github.com/rfordatascience/tidytuesday) is a weekly social data project. All are welcome to participate!  
            - Please remember to share the code used to generate your results!  
            - **TidyTuesday** is organized by the [Data Science Learning Community](https://dslc.io).  
            - [Join our Slack](https://dslc.io/join) for free online help with R, Python, and other data-related topics, or to participate in a data-related book club!
            """, unsafe_allow_html=True)

    # Goals Section
    with st.sidebar:
        with st.expander("__🎯 Goals__"):
            st.markdown("""
            Our over-arching goal for **TidyTuesday** is to provide real-world datasets so that people can learn to work with data.  
            - ✅ **For 2024**, our goal was to be used in at least **10 courses**. Our survey indicates that we are used in at least **30 courses**!  
            - ⏳ **For 2025**, our goal is to **crowdsource the curation of TidyTuesday datasets**.
            """, unsafe_allow_html=True)

    # How to Participate Section
    with st.sidebar:
        with st.expander("__🚀 How to Participate__"):
            st.markdown("""
            - Data is [posted to social media](dataset_announcements.md) every Monday morning.  
            - [Explore the data](https://r4ds.hadley.nz/), watching out for interesting relationships.  
            - **Do not draw conclusions about causation**, as data can have moderating variables.  
            - Use the dataset for **data tidying, visualization, and modeling**.  
            - Create **visualizations, models, Quarto reports, Shiny apps**, or other data science projects.  
            - [Share your work](sharing.md) using the hashtag **#TidyTuesday**.
            """, unsafe_allow_html=True)

    # PydyTuesday Section
    with st.sidebar:
        with st.expander("__🐍 PydyTuesday: A Posit Collaboration__"):
            st.markdown("""
            - **Exploring TidyTuesday data in Python?** Posit has extra resources for you!  
            - Try making a [Quarto dashboard](https://quarto.org/docs/dashboards/).  
            - Find videos and resources in [Posit's PydyTuesday repo](https://github.com/posit-dev/python-tidytuesday-challenge).  
            - Share your work with the world using **#TidyTuesday** and **#PydyTuesday**.  
            - Deploy your work easily with [Connect Cloud](https://connect.posit.cloud/).  
            - You can also [curate a dataset for a future TidyTuesday](.github/pr_instructions.md)!  
            """, unsafe_allow_html=True)

    # Add a note at the bottom of the sidebar
    st.sidebar.markdown(
        """
        ---
        💡 **This Streamlit application was developed by [Francisco Alfaro](https://github.com/fralfaro).**
        """
    )

    return None



# Define the cs_body() function
def cs_body():
    st.title("📊 TidyTuesday Data Explorer")

    image = Image.open(ImagesURL.icon)
    st.image(image, width=600)

    # List of available TidyTuesday years
    years = list(range(2018, 2026))[::-1]

    # Function to fetch the README content from GitHub
    @st.cache_data
    def get_readme_content(year):
        url = f"https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/{year}/readme.md"
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None

    tab1, tab2 = st.tabs(["📊 TidyTuesday by Year", "📊 TidyTuesday by Dataset"])

    with tab1:
        tabs = st.tabs([f"{year}" for year in years])

        for tab, year in zip(tabs, years):
            with tab:
                st.subheader(f"TidyTuesday Dataset for {year}")
                readme_content = get_readme_content(year)
                table_lines = list(filter(lambda line: "|" in line and not any(excl in line for excl in ["[Link]", " ---", "Link "]), (line.strip() for line in readme_content.split('\n'))))
                table_text =  "\n \n" + "\n".join(table_lines)
                file_path = "tidytuesday.md"
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(table_text)
                with open(file_path, "r", encoding="utf-8") as file:
                    markdown_content = file.read()
                st.markdown(markdown_content, unsafe_allow_html=True)
    
    with tab2:
        def fetch_markdown(url):
            try:
                response = requests.get(url)
                response.raise_for_status()
                return response.text
            except requests.exceptions.RequestException as e:
                return f"Error loading file: {e}"

        text = ""
        years = list(range(2019, 2026))[::-1]
        for year in years:
            readme_content = get_readme_content(year)
            text += readme_content

        pattern = r"`(\d{4}-\d{2}-\d{2})`"      
        dates_list = re.findall(pattern, text)
        df = pd.DataFrame(dates_list, columns=["Date"])
        df["Date"] = pd.to_datetime(df["Date"])
        available_years = df["Date"].dt.year.unique()
        selected_year = st.selectbox("Select a year", available_years)
        filtered_dates = df[df["Date"].dt.year == selected_year]["Date"].dt.strftime("%Y-%m-%d").tolist()

        if filtered_dates:
            selected_date = st.selectbox("Select a date", filtered_dates)
            path = f"https://github.com/rfordatascience/tidytuesday/tree/main/data/{selected_year}/{selected_date}/readme.md"
            st.write(f"🔗 link: **{path}**")
            path = f"https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/{selected_year}/{selected_date}/readme.md"
            markdown_content = fetch_markdown(path)
            st.markdown(markdown_content)

    css = '''
    <style>
        /* Adjust the text size in the Tabs */
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
            font-size: 1.5rem; /* Text size in the tabs */
        }

        /* Additional option: Adjust the header size within expanders */
        .st-expander h1, .st-expander h2, .st-expander h3 {
            font-size: 4rem; /* Header size within expanders */
        }

        /* Adjust the text size of the selectbox in the sidebar */
        .sidebar .stSelectbox label {
            font-size: 1.5rem; /* Adjust this value to change the text size */
        }

    </style>
    '''

    st.markdown(css, unsafe_allow_html=True)

    return None

if __name__ == "__main__":
    main()
