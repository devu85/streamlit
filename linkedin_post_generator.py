import streamlit as st
pip install streamlit transformers
from transformers import pipeline

# Load the text generation model
@st.cache_resource
def load_text_generator():
    return pipeline("text-generation", model="gpt2")

# App title
st.title("LinkedIn Post Generator")

# Input fields
topic = st.text_input("Enter the topic for your LinkedIn post:", placeholder="e.g., Leadership, AI, Productivity")
word_count = st.slider("Select the number of words for the post:", min_value=50, max_value=300, step=10, value=100)
tone = st.selectbox("Select the tone of the post:", options=["Professional", "Inspirational", "Casual", "Persuasive"])

# Generate button
if st.button("Generate LinkedIn Post"):
    if not topic:
        st.warning("Please enter a topic before generating the post.")
    else:
        # Load the generator
        text_generator = load_text_generator()

        # Construct the prompt
        prompt = f"Write a {tone.lower()} LinkedIn post about {topic} in {word_count} words."

        # Generate the post
        with st.spinner("Generating your LinkedIn post..."):
            generated_text = text_generator(prompt, max_length=word_count, num_return_sequences=1)[0]["generated_text"]

        # Display the generated post
        st.subheader("Generated LinkedIn Post:")
        st.write(generated_text)

# Sidebar for additional information
st.sidebar.title("About")
st.sidebar.info(
    """
    This app helps you create LinkedIn posts by generating text based on your input.
    Powered by GPT-2 text generation model. Adjust the tone and word count for customized posts!
    """
)
