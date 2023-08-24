import gradio as gr
from ui import themes, generate, vc_batch, with_llm, settings
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--colab", action="store_true", help="Launch in colab")
iscolab = parser.parse_args().colab

with gr.Blocks(themes.Seafoam()) as app:
    with gr.Tabs():
        generate.ui()
        with_llm.ui()
        vc_batch.ui()
        settings.ui()


if iscolab:
  app.queue().launch(share=True)
else:
  app.queue().launch()
