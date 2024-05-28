import streamlit as st
import requests
import json

# Define your domain-specific keywords
education_keywords = ["university", "college", "course", "degree", "admission", 
    "education", "career", "job", "internship", "scholarship", 
    "study", "exam", "roadmap", "class", "student", "professor", 
    "campus", "lecture", "assignment", "diploma", "graduation", 
    "coursework", "thesis", "research", "learning", "academics", 
    "curriculum", "semester", "grad school", "undergraduate", 
    "postgraduate", "bachelor's", "master's", "doctorate", 
    "academic", "syllabus", "textbook", "library", "laboratory", 
    "lecture hall", "dormitory", "residence", "student life", 
    "student union", "major", "minor", "gpa", "dean", "registrar", 
    "alumni", "networking", "career services", "job fair", "resume", 
    "cover letter", "interview", "intern", "apprenticeship", "mentor", 
    "mentorship", "professional development", "skill set", "qualification", 
    "certification", "licensing", "continuing education", "distance learning", 
    "online course", "e-learning", "mooc", "certificate program", "workshop", 
    "conference", "seminar", "symposium", "panel discussion", "lecture series", 
    "academic advising", "career counseling", "guidance counselor", 
    "student advisor", "faculty advisor", "study abroad", "exchange program", 
    "international student", "foreign language", "cross-cultural experience", 
    "diversity", "inclusion", "equity", "accessibility", "financial aid", 
    "grants", "loans", "tuition", "fees", "scholarly", "academic journal", 
    "peer-reviewed", "publication", "citation", "research paper", 
    "thesis statement", "hypothesis", "experiment", "data analysis", 
    "statistical analysis", "conclusion", "abstract", "literature review", 
    "methodology", "results", "discussion", "acknowledgments", "references", 
    "bibliography", "citation style", "mla", "apa", "chicago style", 
    "harvard style", "plagiarism", "academic integrity", "academic honesty", 
    "study skills", "time management", "note-taking", "critical thinking", 
    "problem-solving", "communication skills", "presentation skills", 
    "teamwork", "collaboration", "leadership", "decision-making", 
    "project management", "adaptability", "flexibility", "resilience", 
    "stress management", "wellness", "mental health", "counseling services", 
    "health promotion", "exercise", "nutrition", "sleep hygiene", "self-care", 
    "work-life balance", "productivity", "procrastination", "motivation", 
    "goal setting", "achievement", "success", "fulfillment", "satisfaction", 
    "happiness", "growth", "development", "lifelong learning", 
    "continuous improvement", "personal development", "professional growth", 
    "career advancement", "career path", "career goals", "career change", 
    "job satisfaction", "job security", "economic stability", "financial planning", 
    "retirement", "pension", "savings", "investment", "entrepreneurship", 
    "start-up", "small business", "innovation", "creativity", "risk-taking", 
    "problem-solving", "decision-making", "leadership", "management", 
    "business administration", "marketing", "sales", "finance", "accounting", 
    "human resources", "operations", "logistics", "supply chain", 
    "customer service", "public relations", "communication", "media", 
    "journalism", "broadcasting", "advertising", "branding", "social media", 
    "digital marketing", "technology", "information technology", 
    "computer science", "software engineering", "web development", 
    "data science", "artificial intelligence", "machine learning", "robotics", 
    "automation", "internet of things", "cybersecurity", "network security", 
    "cryptography", "ethical hacking", "biotechnology", "pharmaceuticals", 
    "healthcare", "medicine", "nursing", "allied health", "therapy", "counseling", 
    "psychology", "psychiatry", "social work", "community service", 
    "non-profit", "volunteering", "advocacy", "activism", "environmentalism", 
    "sustainability", "conservation", "renewable energy", "climate change", 
    "green technology", "ecology", "biology", "chemistry", "physics", 
    "mathematics", "statistics", "engineering", "civil engineering", 
    "mechanical engineering", "electrical engineering", "aerospace engineering", 
    "chemical engineering", "industrial engineering", "environmental engineering", 
    "materials science", "nanotechnology", "astronomy", "astrophysics", 
    "cosmology", "geology", "geography", "oceanography", "meteorology", 
    "archaeology", "anthropology", "sociology", "history", "political science", 
    "economics", "international relations", "philosophy", "theology", 
    "religious studies", "languages", "linguistics", "literature", "writing"]

# Define common greetings
greetings = ["hi", "hello", "hey", "hii"]

def is_relevant_query(query, keywords):
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in keywords)

def is_greeting(query, greetings):
    query_lower = query.lower()
    return any(greeting in query_lower for greeting in greetings)

def get_ai_response(input_text, api_key, conversation_history):
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": conversation_history + [
            {"role": "user", "content": input_text}
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "Error: Failed to get response from OpenAI API"

def main():
    st.title("Education and Career Counsellor Chatbot")
    st.write("Hi there! How can I assist you today?")

    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = [{"role": "system", "content": "You are a helpful assistant."}]
        st.session_state.chat_log = []

    user_input = st.text_input("Type your message...")

    api_key = st.secrets["OPENAI_API_KEY"]  # Retrieve API key from Streamlit Secrets

    if st.button("Send"):
        if user_input:
            if is_greeting(user_input, greetings):
                response = "Hello! How can I assist you with your education or career today?"
            elif is_relevant_query(user_input, education_keywords):
                st.session_state.conversation_history.append({"role": "user", "content": user_input})
                response = get_ai_response(user_input, api_key, st.session_state.conversation_history)
                st.session_state.conversation_history.append({"role": "assistant", "content": response})
            else:
                response = "I'm sorry, I can only answer questions related to education and career topics."

            st.session_state.chat_log.append(("You", user_input))
            st.session_state.chat_log.append(("Counsellor", response))

    # Display the conversation history
    for sender, message in st.session_state.chat_log:
        if sender == "You":
            st.write(f"You: {message}")
        elif sender == "Counsellor":
            st.write(f"Counsellor: {message}")

if __name__ == "__main__":
    main()
