import sys
sys.path.append('tts')
sys.path.append('tts/text')
sys.path.append('vc')
sys.path.append('vc/infer_pack')
sys.path.append('llm')


from vc import vc_interface
from tts import tts_interface
from llm import llm_interface
import gradio as gr
import numpy as np

import json


# load vits model names
with open('tts/models/model_list.json', 'r', encoding="utf-8") as file:
    global lang_dic
    lang_dic = json.load(file)

with open('ui/speaker_presets.json', 'r', encoding="utf-8") as file:
    global presets
    presets = json.load(file)


def generate_dialogues(dialogues, selected_presets, llm_output, silence_duration):
    audio_data = {}
    for preset_name in dialogues:
        if preset_name in selected_presets:
            preset = presets[preset_name]
            model = tts_interface.load_model(lang_dic[preset['lang']])
            if preset['vcid'] != 'No conversion':
                hubert_model = vc_interface.load_hubert()
                vc, net_g = vc_interface.get_vc(preset['vcid'])

            for key in dialogues[preset_name]:
                phonemes, audio = tts_interface.generate_speech(model, preset['lang'], dialogues[preset_name][key], int(preset['sid']), False)
                # Scale float32 samples to int16 range
                scaled_audio = (audio[1] * 32767).astype(np.int16)
                audio = (audio[0], scaled_audio)

                if preset['vcid'] != 'No conversion':
                    audio = vc_interface.convert_voice(hubert_model, vc, net_g, audio, preset['vcid'], preset['pitch'], preset['f0method'])

                audio_data[key] = audio

    return llm_output, vc_interface.concat_audio(audio_data, silence_duration)


def generate_with_llm(prompt, selected_presets, temperature, max_tokens, silence_duration):
    if max_tokens == 0:
        max_tokens = None
    executor = llm_interface.set_description_agent(temperature, max_tokens)

    # suffix = '\n登場人物は以下です。\n' + ', '.join(selected_presets)
    suffix = '\nThe characters are as follows\n' + ', '.join(selected_presets)
    dialogues, llm_output = executor.run(prompt + suffix)
    return generate_dialogues(dialogues, selected_presets, llm_output, silence_duration)


def generate(llm_output, selected_presets, silence_duration):
    dialogues = llm_interface.parse(llm_output).return_values['output'][0]
    return generate_dialogues(dialogues, selected_presets, llm_output, silence_duration)


top = '''
  <div align="center">
  See here for instructions on how to use it.

  [English](https://github.com/log1stics/voice-generator-webui/blob/main/docs/how_llm.md) | [日本語](https://github.com/log1stics/voice-generator-webui/blob/main/docs/ja/how_llm.md)

  </div>
'''

default_pr = '''以下の条件を守りなさい
・AIについての議論を描写すること
・遠回しな発言をする
・ケンの葛藤を描くこと
・ケンとカナのすれ違いを描きなさい

・ミカは性格描写は天真爛漫
・カナは性格描写は内気
'''

def ui():
    with gr.TabItem('With LLM'):
        gr.Markdown(top)
        with gr.Row():
            with gr.Column():
                presets_dropdown = gr.Dropdown(choices=list(presets.keys()), label="Presets", multiselect=True)
                
                prompt = gr.Textbox(label="Prompt", value=default_pr, lines=8)
                temperature = gr.Slider(minimum=0, maximum=1, step=0.01, label='Temperature', value=0)
                max_tokens = gr.Slider(minimum=0, maximum=3800, step=1, label='Max Tokens', info='0 means max', value=0)
                silence_duration = gr.Slider(minimum=0, maximum=4, step=0.1, label='Silence Duration (seconds)', value=0.2)

            with gr.Column(scale=1.4):
                llm_output = gr.Textbox(label="LLM Output", interactive=True)
                generate_with_llm_bt = gr.Button("Generate with LLM", variant="primary")
                generate_bt = gr.Button("Generate", variant="primary")
                # clear = gr.Button("Clear")
                
        with gr.Row():
            output_audio = gr.Audio(label="Output Audio", type='numpy')
            generate_with_llm_bt.click(
                fn=generate_with_llm,
                inputs=[prompt, presets_dropdown, temperature, max_tokens, silence_duration],
                outputs=[llm_output, output_audio]
            )
            generate_bt.click(
                fn=generate,
                inputs=[llm_output, presets_dropdown, silence_duration],
                outputs=[llm_output, output_audio]
            )
            # clear.click(lambda: None, None, chatbot, queue=False)
