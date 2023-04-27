import pathlib
import numpy as np
import torch

from .infer_pack.models import SynthesizerTrnMs256NSFsid, SynthesizerTrnMs256NSFsid_nono
from .vc_infer_pipeline import VC
from fairseq import checkpoint_utils
from scipy.signal import resample

from scipy.io import wavfile

device = "cuda:0"  # or cpu
is_half = True  # NVIDIA 20 series and higher GPUs are half-precise with no change in quality


def get_vc(sid):
    weight_root = "vc/models"
    person = f"{weight_root}/{sid}/{sid}.pth"
    global cpt
    # global n_spk, tgt_sr, net_g, vc
    # if (sid == []):
    #     global hubert_model
    #     if (hubert_model != None):
    #         print("clean_empty_cache")
    #         del net_g, n_spk, vc, hubert_model, tgt_sr  # cpt
    #         hubert_model = net_g = n_spk = vc = hubert_model = tgt_sr = None
    #         torch.cuda.empty_cache()
    #         if_f0 = cpt.get("f0", 1)
    #         if (if_f0 == 1):
    #             net_g = SynthesizerTrnMs256NSFsid(*cpt["config"], is_half=is_half)
    #         else:
    #             net_g = SynthesizerTrnMs256NSFsid_nono(*cpt["config"])
    #         del net_g, cpt
    #         torch.cuda.empty_cache()
    #         cpt = None
    #     return {"visible": False, "__type__": "update"}
    # person = "%s/%s" % (weight_root, sid)

    cpt = torch.load(person, map_location="cpu")
    tgt_sr = cpt["config"][-1]
    cpt["config"][-3] = cpt["weight"]["emb_g.weight"].shape[0]  # n_spk
    if_f0 = cpt.get("f0", 1)
    if (if_f0 == 1):
        net_g = SynthesizerTrnMs256NSFsid(*cpt["config"], is_half=is_half)
    else:
        net_g = SynthesizerTrnMs256NSFsid_nono(*cpt["config"])

    del net_g.enc_q
    net_g.load_state_dict(cpt["weight"], strict=False)
    net_g.eval().to(device)

    if (is_half):
        net_g = net_g.half()
    else:
        net_g = net_g.float()
    vc = VC(tgt_sr, device, is_half)
    n_spk = cpt["config"][-3]

    # return {"visible": True,"maximum": n_spk, "__type__": "update"}
    return vc, net_g


def load_hubert():
    # global hubert_model
    models, saved_cfg, task = checkpoint_utils.load_model_ensemble_and_task(["vc/models/hubert_base.pt"], suffix="",)
    hubert_model = models[0]
    hubert_model = hubert_model.to(device)
    if (is_half):
        hubert_model = hubert_model.half()
    else:
        hubert_model = hubert_model.float()
    hubert_model.eval()

    return hubert_model


# need to convert to 16000Hz/np.float32 for RVC input
# VITS output is originally np.float32, so just convert sampling rate
def load_audio(input_audio):
    sr, audio = input_audio
    original_sr = sr
    target_sr = 16000
    original_length = len(audio)
    target_length = int(original_length * (target_sr / original_sr))

    return resample(audio, target_length)


def load_wav(path):
    original_sr, audio = wavfile.read(path)
    audio = audio.astype(np.float32) / 32768.0
    original_length = len(audio)
    target_sr = 16000
    target_length = int(original_length * (target_sr / original_sr))

    return resample(audio, target_length)


def convert_voice(hubert_model, model, net_g, input_audio, vcid, f0_up_key, f0_method):
    # RVC model speaker id
    sid = 0
    # f0_method = "pm"
    # exp = 'simple'
    # f0_up_key = 0.0
    f0_file = None
    index_rate = 1

    file_index = f"vc/models/{vcid}/added.index"
    file_big_npy = f"vc/models/{vcid}/total_fea.npy"

    f0_up_key = int(f0_up_key)
    audio = load_audio(input_audio)
    times = [0, 0, 0]

    # get from cpt
    if_f0 = cpt.get("f0", 1)
    sr = int(cpt.get("sr", 1).replace("k", "")) * 1000

    return sr, model.pipeline(hubert_model, net_g, sid, audio, times, f0_up_key, f0_method, file_index, file_big_npy, index_rate, if_f0, f0_file=f0_file)


def batch_convert(input_dir, output_dir, hubert_model, model, net_g, vcid, f0_up_key, f0_method):
    for wav_path in pathlib.Path(input_dir).glob("*.wav"):
        print(f'Converting {wav_path}')
        audio = wavfile.read(wav_path)
        sr, output_audio = convert_voice(hubert_model, model, net_g, audio, vcid, f0_up_key, f0_method)
        wavfile.write(f'{output_dir}/{wav_path.name}', sr, output_audio)
    print('Done')

# silence_duration is measured in float seconds
def concat_audio(audio_data, silence_duration):
    target_sample_rate = 44100

    resampled_audios = []
    # for audio in audio_data:
    for key in sorted(audio_data.keys()):
        original_rate, original_data = audio_data[key]

        # resample to target_sample_rate
        resampled_data = resample(original_data, num=target_sample_rate * len(original_data) // original_rate)
        resampled_audios.append(resampled_data)



    # make silence NumPy array
    silence_samples = int(target_sample_rate * silence_duration)
    silence_data = np.zeros(silence_samples)
    # concatenate without silence
    # concatenated_audio = np.concatenate(resampled_audios)
    # concatenate resampled audio data and blank data
    concatenated_audio = np.concatenate([
            np.hstack((resampled_audio, silence_data)) for resampled_audio in resampled_audios[:-1]] + [resampled_audios[-1]])

    return target_sample_rate, concatenated_audio


if __name__ == '__main__':
    hubert_model = load_hubert()
    vc, net_g = get_vc('simple')
