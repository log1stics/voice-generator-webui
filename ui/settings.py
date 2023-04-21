import gradio as gr
import os

def set_api_key(llm_api_key):
    os.environ["OPENAI_API_KEY"] = llm_api_key


def ui():
    with gr.TabItem('Settings'):
        with gr.Accordion("LLM API KEY", open=False):
            llm_api_key = gr.Textbox(label='', interactive=True)
            llm_api_key.change(set_api_key, llm_api_key)
