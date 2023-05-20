import torch
from espnet2.bin.tts_inference import Text2Speech

def load_model(name):
    model = Text2Speech.from_pretrained(
        model_file=f"tts/models/{name}.pth",
        device="cuda",
        speed_control_alpha=1,
        use_att_constraint = False,
        noise_scale=0.333,
        noise_scale_dur=0.333,
    )
    return model

def generate_speech(model, text, speed):
    model.decode_conf.update({'alpha': 1 / speed})
    with torch.no_grad():
        wav = model(text)

    return (22050, wav["wav"].view(-1).cpu().numpy())
