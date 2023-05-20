import gradio as gr
from vc import vc_interface
from tts import espnet_interface
from scripts import download
import os
import json


model_dic = {
    "男性": "finetune50epoch_jvs001_jsut",
    "女性": "finetune50epoch_jvs010_jsut"
}

vc_models = ['No conversion']
# load rvc model names
os.makedirs('vc/models', exist_ok=True)
vc_model_root = 'vc/models'
vc_models.extend([d for d in os.listdir(vc_model_root) if os.path.isdir(os.path.join(vc_model_root, d))])


def model_change(lang):
    global model
    global speaker_list

    download.get_espnet_model(model_dic[lang])

    model = espnet_interface.load_model(model_dic[lang])


def vc_change(vcid):
    if vcid != 'No conversion':
        global hubert_model, vc, net_g
        hubert_model = vc_interface.load_hubert()
        vc, net_g = vc_interface.get_vc(vcid)


def text2speech(text, vcid, pitch, f0method, length_scale):
    tts_audio = espnet_interface.generate_speech(model, text, length_scale)
    if vcid != 'No conversion':
        return vc_interface.convert_voice(hubert_model, vc, net_g, tts_audio, vcid, pitch, f0method)

    return tts_audio


def ui():
    with gr.TabItem('ESPnet'):
        gr.Markdown('`pip install espnet`が必要\nアクセント編集不可だが発音の精度が良い')
        with gr.Row():
            with gr.Column(scale=2):
                text = gr.Textbox(label="Text", value="こんにちは、世界", lines=8)
                text2speech_bt = gr.Button("Generate From Text", variant="primary")

            with gr.Column():
                model_dropdown = gr.inputs.Dropdown(choices=list(model_dic.keys()), label="Model",)
                model_dropdown.change(
                    fn=model_change,
                    inputs=[model_dropdown]
                )
                speed = gr.Slider(minimum=0.1, maximum=2, step=0.1, label='Speed', value=1)

                vcid = gr.inputs.Dropdown(choices=vc_models, label="Voice Conversion", default='No conversion')
                vcid.change(
                    fn=vc_change,
                    inputs=[vcid]
                )
                with gr.Accordion("VC Setteings", open=False):
                    pitch = gr.Slider(minimum=-12, maximum=12, step=1, label='Pitch', value=0)
                    f0method = gr.Radio(label="Pitch Method pm: speed-oriented, harvest: accuracy-oriented", choices=["pm", "harvest"], value="pm")


        with gr.Row():
            output_audio = gr.Audio(label="Output Audio", type='numpy')
            text2speech_bt.click(
                fn=text2speech,
                inputs=[text, vcid, pitch, f0method, speed],
                outputs=[output_audio]
            )

