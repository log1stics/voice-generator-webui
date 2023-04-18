import sys
sys.path.append('ui')


import gradio as gr
from ui import themes, generate, vc_batch, train, settings


seafoam = themes.Seafoam()

top = '''
  <div align="center">
  <a href="https://twitter.com/q107z"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/Logo_of_Twitter%2C_Inc..svg/292px-Logo_of_Twitter%2C_Inc..svg.png" width="30"></a>
  </div>
  <br>
'''

with gr.Blocks(theme=seafoam) as app:
    gr.Markdown(top)
    with gr.Tabs():
        generate.ui()
        vc_batch.ui()
        # train.ui()

app.launch()
