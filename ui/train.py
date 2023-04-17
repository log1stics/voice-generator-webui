import gradio as gr


md = '''
以下のリンクからColab環境のT4 GPU(VARM 16GB)を用いて、数クリックで学習できます。
'''

def ui():
    with gr.TabItem('Train'):
        gr.Markdown(md)