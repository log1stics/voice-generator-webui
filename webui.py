import gradio as gr
from ui import themes, generate, generate_with_espnet, vc_batch, with_llm, settings
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--colab", action="store_true", help="Launch in colab")
iscolab = parser.parse_args().colab


seafoam = themes.Seafoam()

top = '''
  <div align="center">
  <a href="https://twitter.com/q107z"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Logo_of_Twitter.svg/292px-Logo_of_Twitter.svg.png" width="30"></a>
  </div>
  <br>
'''

with gr.Blocks(theme=seafoam) as app:
    gr.Markdown(top)
    with gr.Tabs():
        generate.ui()
        generate_with_espnet.ui()
        with_llm.ui()
        vc_batch.ui()
        settings.ui()


if iscolab:
  app.queue().launch(share=True)
else:
  app.queue().launch()
