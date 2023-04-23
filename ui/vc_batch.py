from vc import vc_interface
import gradio as gr
import os


vc_models=['No conversion']
# load rvc model names
vc_model_root = 'vc/models'
vc_models.extend([d for d in os.listdir(vc_model_root) if os.path.isdir(os.path.join(vc_model_root, d))])



def start_batch(input_dir, output_dir, vcid, pitch, f0method):
    hubert_model = vc_interface.load_hubert()
    vc, net_g = vc_interface.get_vc(vcid)
    vc_interface.batch_convert(input_dir, output_dir, hubert_model, vc, net_g, vcid, pitch, f0method)
    return 0


def ui():
    with gr.TabItem('Batch'):
        with gr.Row():
            # with gr.Column():
            # input_dir = gr.File(label="音声ファイルのあるディレクトリ", file_count='directory')
            input_dir = gr.Textbox(label="Input Directory", value="path/to/dir", interactive=True)
            # input_dir.upload(
            #     fn=sam,
            #     inputs=[input_dir],
            #     outputs=[gr.File(label="出力ファイル", file_count='directory')]
            # )
        with gr.Row():
            with gr.Column():
                vcid = gr.inputs.Dropdown(choices=vc_models, label="Voice Conversion", default='No conversion')

                pitch = gr.Slider(minimum=-12, maximum=12, step=1, label='Pitch', value=0)
                f0method = gr.Radio(label="Pitch Method pm: speed-oriented, harvest: accuracy-oriented", choices=["pm", "harvest"], value="pm")
                output_dir = gr.Textbox(label="Output Directory", value="path/to/dir", interactive=True)

                generate_bt = gr.Button("Start Conversion", variant="primary")
                generate_bt.click(
                    fn=start_batch,
                    inputs=[input_dir, output_dir, vcid, pitch, f0method],
                    # outputs=[phonemes, gr.Audio(label="出力オーディオ", type='numpy')]
                )
