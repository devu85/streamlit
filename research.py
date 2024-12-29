try:
    import streamlit as st
    import requests
    from transformers import pipeline

    # Streamlit App Title
    st.title("Research Paper Summarizer")

    # User Input: Interest and Time Period
    interest = st.text_input("Enter your interest (e.g., climate change, AI, etc.):")
    time_period = st.text_input("Enter the time period (e.g., last 5 years, 2020-2023):")

    # Button to Fetch and Summarize Research Papers
    if st.button("Fetch and Summarize"):
        if interest:
            st.write(f"Fetching research papers on: **{interest}** for the period: **{time_period}**...")

            # Function to Fetch Research Papers Using SerpAPI (Google Scholar Engine)
            def fetch_research_papers(interest, time_period):
                api_key = st.secrets["api_keys"]["serpapi_key"]
                query = f"https://serpapi.com/search?engine=google_scholar&q={interest}&api_key={api_key}"
                response = requests.get(query)

                if response.status_code == 200:
                    results = response.json().get("organic_results", [])
                    papers = []
                    for result in results:
                        papers.append({
                            "title": result.get("title", "No title available"),
                            "abstract": result.get("snippet", "No abstract available")
                        })
                    return papers
                else:
                    st.write("Error fetching research papers. Check the API key or query.")
                    return []

            # Fetch research papers
            papers = fetch_research_papers(interest, time_period)

            if papers:
                summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
                st.write("### Summaries of Research Papers")

                for paper in papers:
                    title = paper.get("title", "No title available")
                    abstract = paper.get("abstract", "No abstract available")

                    if abstract:
                        summary = summarizer(abstract, max_length=50, min_length=25, do_sample=False)
                        st.write(f"**Title:** {title}")
                        st.write(f"**Summary:** {summary[0]['summary_text']}")
                        st.write("---")
                    else:
                        st.write(f"**Title:** {title}")
                        st.write("**Summary:** No abstract available to summarize.")
                        st.write("---")
            else:
                st.write("No research papers found for the given interest and time period.")
        else:
            st.write("Please enter an interest to search.")

except ModuleNotFoundError as e:
    print("A required module is missing. Please ensure that all dependencies, including 'streamlit' and 'transformers', are installed.")
    print(e)
