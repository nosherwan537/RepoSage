import gradio as gr
from qa_interface import build_qa_chain

qa = build_qa_chain()

def ask_question(message, history):
    result = qa(message)
    answer = result["result"]
    return answer


gr.ChatInterface(ask_question, title="💬 RepoSage: Chat with Any GitHub Repo").launch()
