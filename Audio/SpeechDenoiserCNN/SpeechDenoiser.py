from tensorflow.keras.layers import Conv2D, Input, LeakyReLU, Flatten, Dense, Reshape, Conv2DTranspose, BatchNormalization, Activation
from tensorflow.keras import Model, Sequential

from SpeechDenoiserCNN.FeatureExtractor import FeatureExtractor
import sounddevice as sd
import tensorflow as tf
import numpy as np
import librosa
import pyaudio
import scipy
import socket
import struct
import audioop
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

windowLength = 256
overlap      = round(0.25 * windowLength) # overlap of 75%
ffTLength    = windowLength
inputFs      = 48e3
fs           = 16e3
numFeatures  = ffTLength//2 + 1
numSegments  = 8


class SpeechDenoiser:
    
    def read_audio(self,filepath, sample_rate, normalize=True):
        audio, sr = librosa.load(filepath, sr=sample_rate)
        if normalize:
            div_fac = 1 / np.max(np.abs(audio)) / 3.0
            audio = audio * div_fac
        return audio, sr

    def build_model(self,l2_strength):
        inputs = Input(shape=[numFeatures,numSegments,1])
        x = inputs

        # -----
        x = tf.keras.layers.ZeroPadding2D(((4,4), (0,0)))(x)
        x = Conv2D(filters=18, kernel_size=[9,8], strides=[1, 1], padding='valid', use_bias=False,
                    kernel_regularizer=tf.keras.regularizers.l2(l2_strength))(x)
        x = Activation('relu')(x)
        x = BatchNormalization()(x)

        skip0 = Conv2D(filters=30, kernel_size=[5,1], strides=[1, 1], padding='same', use_bias=False,
                        kernel_regularizer=tf.keras.regularizers.l2(l2_strength))(x)
        x = Activation('relu')(skip0)
        x = BatchNormalization()(x)

        x = Conv2D(filters=8, kernel_size=[9,1], strides=[1, 1], padding='same', use_bias=False,
                    kernel_regularizer=tf.keras.regularizers.l2(l2_strength))(x)
        x = Activation('relu')(x)
        x = BatchNormalization()(x)

        # -----
        x = Conv2D(filters=18, kernel_size=[9,1], strides=[1, 1], padding='same', use_bias=False,
                    kernel_regularizer=tf.keras.regularizers.l2(l2_strength))(x)
        x = Activation('relu')(x)
        x = BatchNormalization()(x)

        skip1 = Conv2D(filters=30, kernel_size=[5,1], strides=[1, 1], padding='same', use_bias=False,
                        kernel_regularizer=tf.keras.regularizers.l2(l2_strength))(x)
        x = Activation('relu')(skip1)
        x = BatchNormalization()(x)

        x = Conv2D(filters=8, kernel_size=[9,1], strides=[1, 1], padding='same', use_bias=False,
                    kernel_regularizer=tf.keras.regularizers.l2(l2_strength))(x)
        x = Activation('relu')(x)
        x = BatchNormalization()(x)

        # ----
        x = Conv2D(filters=18, kernel_size=[9,1], strides=[1, 1], padding='same', use_bias=False,
                    kernel_regularizer=tf.keras.regularizers.l2(l2_strength))(x)
        x = Activation('relu')(x)
        x = BatchNormalization()(x)
        
        x = Conv2D(filters=30, kernel_size=[5,1], strides=[1, 1], padding='same', use_bias=False,
                    kernel_regularizer=tf.keras.regularizers.l2(l2_strength))(x)
        x = Activation('relu')(x)
        x = BatchNormalization()(x)

        x = Conv2D(filters=8, kernel_size=[9,1], strides=[1, 1], padding='same', use_bias=False,
                    kernel_regularizer=tf.keras.regularizers.l2(l2_strength))(x)
        x = Activation('relu')(x)
        x = BatchNormalization()(x)

        # ----
        x = Conv2D(filters=18, kernel_size=[9,1], strides=[1, 1], padding='same', use_bias=False,
                    kernel_regularizer=tf.keras.regularizers.l2(l2_strength))(x)
        x = Activation('relu')(x)
        x = BatchNormalization()(x)

        x = Conv2D(filters=30, kernel_size=[5,1], strides=[1, 1], padding='same', use_bias=False,
                    kernel_regularizer=tf.keras.regularizers.l2(l2_strength))(x)
        x = x + skip1
        x = Activation('relu')(x)
        x = BatchNormalization()(x)

        x = Conv2D(filters=8, kernel_size=[9,1], strides=[1, 1], padding='same', use_bias=False,
                    kernel_regularizer=tf.keras.regularizers.l2(l2_strength))(x)
        x = Activation('relu')(x)
        x = BatchNormalization()(x)

        # ----
        x = Conv2D(filters=18, kernel_size=[9,1], strides=[1, 1], padding='same', use_bias=False,
                    kernel_regularizer=tf.keras.regularizers.l2(l2_strength))(x)
        x = Activation('relu')(x)
        x = BatchNormalization()(x)

        x = Conv2D(filters=30, kernel_size=[5,1], strides=[1, 1], padding='same', use_bias=False,
                    kernel_regularizer=tf.keras.regularizers.l2(l2_strength))(x)
        x = x + skip0
        x = Activation('relu')(x)
        x = BatchNormalization()(x)

        x = Conv2D(filters=8, kernel_size=[9,1], strides=[1, 1], padding='same', use_bias=False,
                    kernel_regularizer=tf.keras.regularizers.l2(l2_strength))(x)
        x = Activation('relu')(x)
        x = BatchNormalization()(x)

        # ----
        x = tf.keras.layers.SpatialDropout2D(0.2)(x)
        x = Conv2D(filters=1, kernel_size=[129,1], strides=[1, 1], padding='same')(x)

        model = Model(inputs=inputs, outputs=x)

        optimizer = tf.keras.optimizers.Adam(3e-4)
        #optimizer = RAdam(total_steps=10000, warmup_proportion=0.1, min_lr=3e-4)

        model.compile(optimizer=optimizer, loss='mse', 
                        metrics=[tf.keras.metrics.RootMeanSquaredError('rmse')])
        return model
    
    def prepare_input_features(self,stft_features):
        # Phase Aware Scaling: To avoid extreme differences (more than
        # 45 degree) between the noisy and clean phase, the clean spectral magnitude was encoded as similar to [21]:
        noisySTFT = np.concatenate([stft_features[:,0:numSegments-1], stft_features], axis=1)
        stftSegments = np.zeros((numFeatures, numSegments , noisySTFT.shape[1] - numSegments + 1))

        for index in range(noisySTFT.shape[1] - numSegments + 1):
            stftSegments[:,:,index] = noisySTFT[:,index:index + numSegments]
        return stftSegments

    def removeNoise(self,features, phase, cleanMean=None, cleanStd=None,noiseAudioFeatureExtractor=None):
        # scale the outpus back to the original range
        if cleanMean and cleanStd:
            features = cleanStd * features + cleanMean

        phase = np.transpose(phase, (1, 0))
        features = np.squeeze(features)

        # features = librosa.db_to_power(features)
        features = features * np.exp(1j * phase)  # that fixes the abs() ope previously done

        features = np.transpose(features, (1, 0))
        return noiseAudioFeatureExtractor.get_audio_from_stft_spectrogram(features)

    def resample_ratecv(self,data,samplerate=48000, resample_rate=16000):
        #Resamples the given PCM stream to resample_rate.
        return audioop.ratecv((bytearray(data)), 2, 1, samplerate, resample_rate, None)

    def get_all_samples(self,data):
        allsamples=[]
        index=0
        while True:
            try:
                index=index+1
                sample=audioop.getsample(data,2,index)
                sample_8a = sample & 0xff
                sample_8b = (sample >> 8) & 0xff
                allsamples.append(int(str(sample_8a)))
                allsamples.append(int(str(sample_8b)))
            except:
                break;

        return allsamples;

    def __init__(self):
        print("Init")
        self.model = self.build_model(l2_strength=0.0)
        self.model.load_weights(os.path.dirname(__file__)+'./model/cnn-audio.h5')

    def reduceNoiseMain(self,noisyAudio):
        noiseAudioFeatureExtractor = FeatureExtractor(noisyAudio, windowLength=windowLength, overlap=overlap, sample_rate=16000)
        noise_stft_features = noiseAudioFeatureExtractor.get_stft_spectrogram()
        noisyPhase = np.angle(noise_stft_features)
        noise_stft_features = np.abs(noise_stft_features)

        mean = np.mean(noise_stft_features)
        std = np.std(noise_stft_features)
        noise_stft_features = (noise_stft_features - mean) / std

        predictors = self.prepare_input_features(noise_stft_features)
        predictors = np.reshape(predictors, (predictors.shape[0], predictors.shape[1], 1, predictors.shape[2]))
        predictors = np.transpose(predictors, (3, 0, 1, 2)).astype(np.float32)

        STFTFullyConvolutional = self.model.predict(predictors)

        denoisedAudioFullyConvolutional = self.removeNoise(STFTFullyConvolutional, noisyPhase, mean, std,noiseAudioFeatureExtractor)

        from scipy.io.wavfile import write as scipyWrite
        scipyWrite('tmp_f.wav', 16000, denoisedAudioFullyConvolutional)

        
        #Test if it worked
        # sd.play(data=noisyAudio , samplerate= fs)

        # import matplotlib.pyplot as plt

        # f, (ax2, ax3) = plt.subplots(2, 1, sharey=True)
        # ax2.plot(noisyAudio)
        # ax2.set_title("Noisy Audio")

        # ax3.plot(denoisedAudioFullyConvolutional)
        # ax3.set_title("Denoised Audio")

        # f.show()

