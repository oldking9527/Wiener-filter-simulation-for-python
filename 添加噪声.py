import soundfile as sf
import math
import librosa
import numpy as np


def add_noise(audio_path, noise_path,out_path, SNR, sr=16000):
    #读取语音文件data和fs
    src, sr = librosa.core.load(audio_path, sr=sr)
    #
    random_values = np.random.rand(len(src))
    #计算语音信号功率Ps和噪声功率Pn1
    Ps = np.sum(src ** 2) / len(src)
    Pn1 = np.sum(random_values ** 2) / len(random_values)

    # 计算k值
    k=math.sqrt(Ps/(10**(SNR/10)*Pn1))
    #将噪声数据乘以k,
    random_values_we_need=random_values*k
    #计算新的噪声数据的功率
    Pn=np.sum(random_values_we_need**2)/len(random_values_we_need)
    #以下开始计算信噪比
    snr=10*math.log10(Ps/Pn)
    print("当前信噪比：",snr)

    #单独将噪音数据写入文件
    sf.write(noise_path,random_values_we_need, sr)
    #将噪声数据叠加到纯净音频上去
    outdata=src+random_values_we_need
    # 将叠加噪声的数据写入文件
    sf.write(out_path, outdata, sr)


def main():

    filename='sf1.wav'
    #纯净语音文件路径
    noisename='noise.wav'
    #产生的噪声数据路径
    outname='add_noise.wav'
    #叠加了噪声后的数据
    SNR=15
    #选定信噪比
    add_noise(filename,noisename,outname,SNR)
    #调用函数，直接生成数据



