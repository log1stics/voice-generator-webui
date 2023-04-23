import gradio as gr
from vc import vc_interface
from tts import tts_interface
from scripts import download
import os
import json

# load vits model names
with open('tts/models/model_list.json', 'r', encoding="utf-8") as file:
    global lang_dic
    lang_dic = json.load(file)


vc_models = ['No conversion']
# load rvc model names
os.makedirs('vc/models', exist_ok=True)
vc_model_root = 'vc/models'
vc_models.extend([d for d in os.listdir(vc_model_root) if os.path.isdir(os.path.join(vc_model_root, d))])


def lang_change(lang):
    global model
    global speaker_list

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
        return phonemes, vc_interface.convert_voice(hubert_model, vc, net_g, tts_audio, vcid, pitch, f0method)

    return phonemes, tts_audio


def acc2speech(lang, text, sid, vcid, pitch, f0method):
    _, tts_audio = tts_interface.generate_speech(model, lang, text, speaker_list.index(sid), True)
    if vcid != 'No conversion':
        return vc_interface.convert_voice(hubert_model, vc, net_g, tts_audio, vcid, pitch, f0method)

    return tts_audio


def save_preset(preset_name, lang_dropdown, sid, vcid, pitch, f0method):
    path = 'ui/speaker_presets.json'
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    data[preset_name] = {}
    data[preset_name]['lang'] = lang_dropdown
    data[preset_name]['sid'] = speaker_list.index(sid)
    data[preset_name]['vcid'] = vcid
    data[preset_name]['pitch'] = pitch
    data[preset_name]['f0method'] = f0method

    # 更新されたデータをJSONファイルに書き込み
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def ui():
    with gr.TabItem('Generate'):
        with gr.Row():
            with gr.Column(scale=2):
                text = gr.Textbox(label="Text", value="こんにちは、世界", lines=8)
                text2speech_bt = gr.Button("Generate From Text", variant="primary")

                phonemes = gr.Textbox(label="Phones", interactive=True, lines=8)
                acc2speech_bt = gr.Button("Generate From Phones", variant="primary")

            with gr.Column():
                lang_dropdown = gr.inputs.Dropdown(choices=list(lang_dic.keys()), label="Languages",)
                sid = gr.inputs.Dropdown(choices=[], label="Speaker")
                lang_dropdown.change(
                    fn=lang_change,
                    inputs=[lang_dropdown],
                    outputs=sid
                )

                vcid = gr.inputs.Dropdown(choices=vc_models, label="Voice Conversion", default='No conversion')
                vcid.change(
                    fn=vc_change,
                    inputs=[vcid]
                )
                with gr.Accordion("VC Setteings", open=False):
                    pitch = gr.Slider(minimum=-12, maximum=12, step=1, label='Pitch', value=0)
                    f0method = gr.Radio(label="Pitch Method pm: speed-oriented, harvest: accuracy-oriented", choices=["pm", "harvest"], value="pm")

                preset_name = gr.Textbox(label="Preset Name", interactive=True)
                save_preset_bt = gr.Button("Save Preset")
                save_preset_bt.click(
                    fn=save_preset,
                    inputs=[preset_name, lang_dropdown, sid, vcid, pitch, f0method],
                )

        with gr.Row():
            output_audio = gr.Audio(label="Output Audio", type='numpy')
            text2speech_bt.click(
                fn=text2speech,
                inputs=[lang_dropdown, text, sid, vcid, pitch, f0method],
                outputs=[phonemes, output_audio]
            )
            acc2speech_bt.click(
                fn=acc2speech,
                inputs=[lang_dropdown, phonemes, sid, vcid, pitch, f0method],
                outputs=[output_audio]
            )
