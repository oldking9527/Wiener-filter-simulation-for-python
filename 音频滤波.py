import librosa
import math
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def wiener_filter(noisy, clean, noise, para):  # 干净的语音信号clean，含噪语音noisy，噪声信号noise，维纳滤波参数para
    n_fft = para["n_fft"]  # 傅里叶变换的点数
    hop_length = para["hop_length"]  # 傅里叶变换窗口长度
    win_length = para["win_length"]
    alpha = para["alpha"]
    beta = para["beta"]

    S_noisy = librosa.stft(noisy, n_fft=n_fft, hop_length=hop_length, win_length=win_length)  # 进行短时傅里叶变换，时域转频域
    S_noise = librosa.stft(noise, n_fft=n_fft, hop_length=hop_length, win_length=win_length)
    S_clean = librosa.stft(clean, n_fft=n_fft, hop_length=hop_length, win_length=win_length)

    Pxx = np.mean((np.abs(S_clean)) ** 2, axis=1, keepdims=True)  # 模值的平方再取均值（期望）
    Pnn = np.mean((np.abs(S_noise)) ** 2, axis=1, keepdims=True)

    H = (Pxx / (Pxx + alpha * Pnn)) ** beta  # 完成滤波器h（n）

    S_enhec = S_noisy * H  # 实施滤波

    enhenc = librosa.istft(S_enhec, hop_length=hop_length, win_length=win_length)  # 短时反式傅里叶变换生成增强信号

    return H, enhenc


def displayWaveform():  # 显示语音时域波形
    samples, sr = librosa.load('sf1.wav', sr=16000)
    # samples = samples[6000:16000]
    samples1, sr = librosa.load('add_noise.wav', sr=16000)
    samples2, sr = librosa.load('enhce.wav', sr=16000)

    print(len(samples), sr)
    time = np.arange(0, len(samples)) * (1.0 / sr)

    print(len(samples1), sr)
    time1 = np.arange(0, len(samples1)) * (1.0 / sr)

    print(len(samples2), sr)
    time2 = np.arange(0, len(samples2)) * (1.0 / sr)

    plt.figure('语音时域波形')
    plt.subplot(131)
    plt.plot(time, samples)
    plt.title("初始信号")
    plt.xlabel("时长（秒）")
    plt.ylabel("振幅")
    # plt.savefig("your dir\语音信号时域波形图", dpi=600)

    plt.subplot(132)
    plt.plot(time1, samples1)
    plt.title("加噪信号")
    plt.xlabel("时长（秒）")
    plt.ylabel("振幅")

    plt.subplot(133)
    plt.plot(time2, samples2)
    plt.title("滤波信号")
    plt.xlabel("时长（秒）")
    plt.ylabel("振幅")
    plt.show()

#def specgram():
    # plt.figure(2)
    # plt.subplot(3, 1, 1)
    # plt.specgram(clean, NFFT=256, Fs=fs)
    # plt.xlabel("clean specgram")
    # plt.subplot(3, 1, 2)
    # plt.specgram(noisy, NFFT=256, Fs=fs)
    # plt.xlabel("noisy specgram")
    # plt.subplot(3, 1, 3)
    # plt.specgram(enhenc, NFFT=256, Fs=fs)
    # plt.xlabel("enhece specgram")
    # plt.show()

def main():

    # 读取干净语音
    clean_wav_file = "sf1.wav"
    clean, fs = librosa.load(clean_wav_file, sr=None)

    # 读取读取噪声语音
    noisy_wav_file = "add_noise.wav"
    noisy, fs = librosa.load(noisy_wav_file, sr=None)

    # 获取噪声
    noise = noisy - clean

    # 设置模型参数
    para_wiener = {}
    para_wiener["n_fft"] = 256
    para_wiener["hop_length"] = 128
    para_wiener["win_length"] = 256
    para_wiener["alpha"] = 1
    para_wiener["beta"] = 5

    # 维纳滤波
    H, enhenc = wiener_filter(noisy, clean, noise, para_wiener)

    sf.write("enhce.wav", enhenc, fs)
    displayWaveform()
    plt.figure('信号光谱图')
    plt.subplot(3, 1, 1)
    plt.title("初始信号")
    plt.specgram(clean, NFFT=256, Fs=fs)
    plt.subplot(3, 1, 2)
    plt.title("加噪信号")
    plt.specgram(noisy, NFFT=256, Fs=fs)
    plt.subplot(3, 1, 3)
    plt.xlabel("滤波信号")
    plt.specgram(enhenc, NFFT=256, Fs=fs)
    plt.show()



