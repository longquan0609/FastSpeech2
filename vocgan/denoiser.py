import sys
import torch
from .utils.stft import STFT


class Denoiser(torch.nn.Module):
    """ Removes model bias from audio produced with waveglow """

    def __init__(self, melgan, filter_length = 1024, n_overlap = 4, win_length = 1024, mode = 'zeros', device = 'cpu'):
        super(Denoiser, self).__init__()
        self.stft = STFT(filter_length = filter_length, hop_length = int(filter_length / n_overlap), win_length = win_length, device = device).to(device)
        if mode == 'zeros':
            mel_input = torch.zeros((1, 80, 88)).to(device)
        elif mode == 'normal':
            mel_input = torch.randn((1, 80, 88)).to(device)
        else:
            raise Exception("Mode {} if not supported".format(mode))

        with torch.no_grad():
            bias_audio = melgan.inference(mel_input).float()  # [B, 1, T]

            bias_spec, _ = self.stft.transform(bias_audio.squeeze(0))

        self.register_buffer('bias_spec', bias_spec[:, :, 0][:, :, None])
        self.device = device
        self.to(device)

    def forward(self, audio, strength = 0.1):
        audio_spec, audio_angles = self.stft.transform(audio.to(self.device).float())
        audio_spec_denoised = audio_spec.to(self.device) - self.bias_spec * strength
        audio_spec_denoised = torch.clamp(audio_spec_denoised, 0.0)
        audio_denoised = self.stft.inverse(audio_spec_denoised, audio_angles.to(self.device))
        return audio_denoised
