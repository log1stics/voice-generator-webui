import sys
sys.path.append('modules')
sys.path.append('tts')
sys.path.append('tts/text')
sys.path.append('vc')
sys.path.append('vc/infer_pack')




import gradio as gr
from vc import vc_interface
from tts import tts_interface
import scripts.download as download
import os
import json

# load vits model names
with open('tts/models/model_list.json', 'r') as file:
    lang_dic = json.load(file)



vc_models=['No conversion']
# load rvc model names
vc_model_root = 'vc/models'
vc_models.extend([d for d in os.listdir(vc_model_root) if os.path.isdir(os.path.join(vc_model_root, d))])


def lang_change(lang):
    global model
    global speaker_list
    global lang_dic

    download.get_vits_model(lang_dic[lang])
    with open(f'tts/models/{lang_dic[lang]}_speakers.txt', "r", encoding="utf-8") as file:
        speaker_list = [line.strip() for line in file.readlines()]


    model = tts_interface.load_model(lang_dic[lang])
    return gr.Dropdown.update(choices=speaker_list)

def vc_change(vcid):
    if vcid != 'No conversion':
        global hubert_model, vc, net_g
        hubert_model = vc_interface.load_hubert()
        vc, net_g = vc_interface.get_vc(vcid)


def text2speech(lang, text, sid, vcid, pitch, f0method):
    phonemes, tts_audio = tts_interface.generate_speech(model, lang, text, speaker_list.index(sid), False)
    if vcid != 'No conversion':
        return phonemes, vc_interface.inf(hubert_model, vc, net_g, tts_audio, vcid, pitch, f0method)

    return phonemes, tts_audio
def acc2speech(lang, text, sid, vcid, pitch, f0method):
    _, tts_audio = tts_interface.generate_speech(model, lang, text, speaker_list.index(sid), True)
    if vcid != 'No conversion':
        return vc_interface.inf(hubert_model, vc, net_g, tts_audio, vcid, pitch, f0method)

    return tts_audio


def ui():
    with gr.TabItem('Generate'):
        with gr.Row():
            with gr.Column(scale=2):
                text = gr.Textbox(label="生成する音声用テキスト", value="こんにちは、世界", lines=8)

                phonemes = gr.Textbox(label="読み・アクセント", interactive=True, lines=8)

            with gr.Column():
                lang_dropdown = gr.inputs.Dropdown(choices=list(lang_dic.keys()), label="言語",)
                sid = gr.inputs.Dropdown(choices=[], label="話者")
                lang_dropdown.change(
                    fn=lang_change,
                    inputs=[lang_dropdown],
                    outputs=sid
                )
                

                vcid = gr.inputs.Dropdown(choices=vc_models, label="変換対象", default='No conversion')
                vcid.change(
                    fn=vc_change,
                    inputs=[vcid]
                )
                with gr.Accordion("変換設定", open=False):
                    pitch = gr.Slider(minimum=-12, maximum=12, step=1, label='ピッチ', value=0)
                    f0method = gr.Radio(label="ピッチ抽出 pm: 速度重視、harvest: 精度重視", choices=["pm", "harvest"], value="pm")

                text2speech_bt = gr.Button("テキストから生成", variant="primary")
                acc2speech_bt2 = gr.Button("アクセントから生成", variant="primary")

        with gr.Row():
            output_audio = gr.Audio(label="出力オーディオ", type='numpy')
            text2speech_bt.click(
                fn=text2speech,
                inputs=[lang_dropdown, text, sid, vcid, pitch, f0method],
                outputs=[phonemes, output_audio]
            )
            acc2speech_bt2.click(
                fn=acc2speech,
                inputs=[lang_dropdown, phonemes, sid, vcid, pitch, f0method],
                outputs=[output_audio]
            )
