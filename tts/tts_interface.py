import torch

from . import commons
from . import utils
from .models import SynthesizerTrn

from .text import symbols
from .text import text_to_sequence

# from scipy.io.wavfile import write


def load_model(name):
    hps = utils.get_hparams_from_file(f"tts/configs/{name}.json")

    if name == 'jvs':
        symbols_len = len(symbols.jvs_symbols)
    else:
        symbols_len = len(symbols.vctk_symbols)

    net_g = SynthesizerTrn(
        symbols_len,
        hps.data.filter_length // 2 + 1,
        hps.train.segment_size // hps.data.hop_length,
        n_speakers=hps.data.n_speakers,
        **hps.model).cuda()
    _ = net_g.eval()

    _ = utils.load_checkpoint(f"tts/models/{name}.pth", net_g, None)
    return net_g


def get_text(text, lang, cleaned):
    clean_text, text_norm = text_to_sequence(text, lang, cleaned)

    text_norm = commons.intersperse(text_norm, 0)  # if add_blank == True:
    text_norm = torch.LongTensor(text_norm)
    return clean_text, text_norm


def generate_speech(net_g, lang, text, sid, cleaned, length_scale):
    length_scale = 1 / length_scale
    clean_text, stn_tst = get_text(text, lang, cleaned)
    with torch.no_grad():
        x_tst = stn_tst.cuda().unsqueeze(0)
        x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).cuda()
        audio = net_g.infer(x_tst, x_tst_lengths, sid=torch.LongTensor([sid]).cuda(), noise_scale=.667, noise_scale_w=0.8, length_scale=length_scale)[0][0, 0].data.cpu().float().numpy()

    return ' '.join(clean_text), (22050, audio)


if __name__ == '__main__':
    pass
    # hps = utils.get_hparams_from_file("./configs/ljs_base.json")
    # model = load_model(hps)

    # generate_speech(model, 'hi', lang='ja')
