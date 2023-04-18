import sys
sys.path.append('ui')


import gradio as gr
from ui import themes, generate, vc_batch, train, settings


seafoam = themes.Seafoam()


with gr.Blocks(theme=seafoam) as app:
    with gr.Tabs():
        generate.ui()
        vc_batch.ui()
        # train.ui()

app.launch()
