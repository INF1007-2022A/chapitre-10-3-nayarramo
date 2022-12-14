#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import wave
import struct
import math
import matplotlib.pyplot as plt
import numpy as np
import scipy


SAMPLING_FREQ = 44100 # Hertz, taux d'échantillonnage standard des CD
SAMPLE_WIDTH = 16 # Échantillons de 16 bit
MAX_INT_SAMPLE_VALUE = 2**(SAMPLE_WIDTH-1) - 1


def merge_channels(channels):
	# Équivalent de :  [sample for samples in zip(*channels) for sample in samples]
	return np.fromiter((sample for samples in zip(*channels) for sample in samples), float)

def separate_channels(samples, num_channels):
	# Équivalent de :  [samples[i::num_channels] for i in range(num_channels)]
	return np.fromiter((samples[i::num_channels] for i in range(num_channels)), float)

def generate_sample_time_points(duration):
	# Générer un tableau de points temporels également espacés en seconde. On a SAMPLING_FREQ points par seconde.
	pass

def sine(freq, amplitude, duration):
	# Générer une onde sinusoïdale à partir de la fréquence et de l'amplitude donnée, sur le temps demandé et considérant le taux d'échantillonnage.
	# Formule de la valeur y d'une onde sinusoïdale à l'angle x en fonction de sa fréquence F et de son amplitude A :
	# y = A * sin(F * x), où x est en radian.
	# Si on veut le x qui correspond au moment t, on peut dire que 2π représente une seconde, donc x = t * 2π,
	# Or t est en secondes, donc t = i / nb_échantillons_par_secondes, où i est le numéro d'échantillon.
	pass

def square(freq, amplitude, duration):
	# Générer une onde carrée d'une fréquence et amplitude donnée.
	pass

def sawtooth(freq, amplitude, duration):
	# Générer une onde en dents de scie (sawtooth) à partir de l'amplitude et fréquence donnée.
	pass

def sine_with_overtones(root_freq, amplitude, overtones, duration):
	# Générer une onde sinusoïdale avec ses harmoniques. Le paramètre overtones est une liste de tuple où le premier élément est le multiple de la fondamentale et le deuxième élément est l'amplitude relative de l'harmonique.
	pass

def normalize(samples, norm_target):
	# Normalisez un signal à l'amplitude donnée
	pass

def convert_to_bytes(samples):
	# Convertir les échantillons en tableau de bytes en les convertissant en entiers 16 bits.
	# Les échantillons en entrée sont entre -1 et 1, nous voulons les mettre entre -MAX_SAMPLE_VALUE et MAX_SAMPLE_VALUE
	# Juste pour être certain de ne pas avoir de problème, on doit clamper les valeurs d'entrée entre -1 et 1.
	pass

def convert_to_samples(bytes):
	# Faire l'opération inverse de convert_to_bytes, en convertissant des échantillons entier 16 bits en échantillons réels
	pass


def main():
	try:
		# On met les fichiers de sortie dans leur propre dossier.
		os.mkdir("output")
	except:
		pass

	# On affiche une onde d'exemple 
	xs = generate_sample_time_points(3)
	ys = square(1.0, 0.5, 3) + sawtooth(10.0, 0.1, 3)
	plt.figure(figsize=(12, 6))
	plt.plot(xs, ys)
	plt.grid(color="wheat")
	plt.ylim([-1.1, 1.1])
	plt.xlim([0, 2])
	plt.xlabel("t (s)")
	plt.ylabel("y")
	plt.show()

	# Exemple d'un la et mi (quinte juste), un dans le channel gauche et l'autre dans le channel droit
	with wave.open("output/perfect_fifth_panned.wav", "wb") as writer:
		# On fait la config du writer (2 channels, échantillons de deux octets, fréquence d'échantillonnage).
		writer.setnchannels(2)
		writer.setsampwidth(2)
		writer.setframerate(SAMPLING_FREQ)

		# On génére un la3 (220 Hz) et un mi4 (intonation juste, donc ratio de 3/2)
		#samples1 = sine(220, 0.9, 30.0)
		samples1 = sawtooth(220, 0.9, 30.0)
		#samples2 = sine(220 * (3/2), 0.7, 30.0)
		samples2 = sawtooth(220 * (3/2), 0.7, 30.0)

		# On met les samples dans des channels séparés (la à gauche, mi à droite)
		merged = merge_channels([samples1, samples2])
		data = convert_to_bytes(merged)

		writer.writeframes(data)

	with wave.open("output/major_chord.wav", "wb") as writer:
		writer.setnchannels(1)
		writer.setsampwidth(2)
		writer.setframerate(SAMPLING_FREQ)

		# Un accord majeur (racine, tierce, quinte, octave) en intonation juste
		root_freq = 220
		root = sine(root_freq, 1, 10.0)
		third = sine(root_freq * 5/4, 1, 10.0)
		fifth = sine(root_freq * 3/2, 1, 10.0)
		octave = sine(root_freq * 2, 1, 10.0)
		# Étant donné qu'on additionne les signaux, on normalize pour que ça soit à un bon niveau.
		chord = normalize(root + third + fifth + octave, 0.89)

		writer.writeframes(convert_to_bytes(chord))

	with wave.open("output/overtones.wav", "wb") as writer:
		writer.setnchannels(1)
		writer.setsampwidth(2)
		writer.setframerate(SAMPLING_FREQ)

		# On génère un signal avec ses 3 premières harmoniques (2x, 3x et 4x la fréquence de base)
		samples = sine_with_overtones(220, 1, [(i, 0.15**(i-1)) for i in range(2, 5)], 10)
		# Encore, on additionne des signaux, donc on normalise.
		samples = normalize(samples, 0.89)

		writer.writeframes(convert_to_bytes(samples))

# def main():
# 	try:
# 		os.mkdir("output")
# 	except:
# 		pass

# 	with wave.open("output/perfect_fifth.wav", "wb") as writer:
# 		writer.setnchannels(2)
# 		writer.setsampwidth(2)
# 		writer.setframerate(SAMPLING_FREQ)

# 		# On génére un la3 (220 Hz) et un mi4 (intonation juste, donc ratio de 3/2)
# 		samples1 = sine(220, 0.4, 30.0)
# 		samples2 = sine(220 * (3/2), 0.3, 30.0)
# 		samples3 = normalize(samples1 + samples2, 0.89)

# 		# On met les samples dans des channels séparés (la à gauche, mi à droite)
# 		merged = merge_channels([samples3, samples3])
# 		data = convert_to_bytes(merged)

# 		writer.writeframes(data)


if __name__ == "__main__":
	main()
