from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
import logging
logging.basicConfig(level = logging.INFO, format = "%(threadName)s - %(message)s")
import scipy.sparse as sc
from scipy.sparse.linalg import spsolve
import tkinter as tk

import base_objects


def solve_derivatives_max(source_path, target_path):
   SCREEN_WIDTH = 1400
   SCREEN_HEIGHT = 850
   fig, axes = plt.subplots(6, figsize=(10, 60))
   #the first two plots are source then target
   """m est le nombre de lignes de la matrice rognée, n est le nombre de colonnes"""

   target = Image.open(target_path).resize((SCREEN_WIDTH, SCREEN_HEIGHT))
   source = Image.open(source_path).resize((SCREEN_WIDTH, SCREEN_HEIGHT))
   source_pos, target_pos = base_objects.tkinter_img_large(source, target)  # [x1,y1,x2,y2], [x1,y1]
   print("sourcepos", source_pos)
   print("target_pos", target_pos)
   if not source_pos:
      raise Exception('tkinter did not receive source image from user')

   source = source.crop(source_pos)
   print(f"working with source shape : ", source.size)
   source = np.asarray(source)
   m, n = source.shape[:2]
   source_dict = {'Reds': source[::, ::, 0],
                  'Greens': source[::, ::, 1], 'Blues': source[::, ::, 2]}

   #make target rectangle of the same size as source

   target_x, target_y = target_pos
   target = target.crop((target_x, target_y, target_x+n, target_y+m))
   target = np.asarray(target)
   target_dict = {'Reds': target[::, ::, 0],
                  'Greens': target[::, ::, 1], 'Blues': target[::, ::, 2]}

   #testing with just the grey version #[0.2989, 0.5870, 0.1140]
   axes[0].imshow(source, vmin=0, vmax=255)
   axes[1].imshow(target, vmin=0, vmax=255)
   #testing with all three versions

   final_arr = np.empty(shape=(m, n, 3))
   A = base_objects.lapAfinal2(m, n)
   for i, c in enumerate(source_dict.keys()):
      source = source_dict[c]
      target = target_dict[c]
      source = source.flatten()
      target = target.flatten()

      #A = lapAfinal2(m,n)
      b = base_objects.make_b_max(m, n, source, target)
      print(f"A.shape", A.shape)
      print(f"b.shape", b.shape)
      x = sc.linalg.spsolve(A, b)

      print("before glueing", x.shape)
      x = base_objects.rebuild_u(x, target.flatten(), m, n)
      print("after glueing", x.shape)
      x[x < 0] = 0
      x[x > 255] = 255
      axes[i+2].imshow(x.astype('uint8'), cmap=c, vmin=0, vmax=255)
      final_arr[::, ::, i] = x
   final_arr = final_arr.astype('uint8')

   final_img = Image.fromarray(final_arr)
   target = Image.open(
       target_path).resize((SCREEN_WIDTH, SCREEN_HEIGHT))
   target.paste(final_img, (target_x, target_y))
   target.show()
   axes[5].imshow(target)


def solve_derivatives_min(source_path, target_path):
   SCREEN_WIDTH = 1400
   SCREEN_HEIGHT = 850
   fig, axes = plt.subplots(6, figsize=(10, 60))
   #the first two plots are source then target
   """m est le nombre de lignes de la matrice rognée, n est le nombre de colonnes"""

   target = Image.open(target_path).resize((SCREEN_WIDTH, SCREEN_HEIGHT))
   source = Image.open(source_path).resize((SCREEN_WIDTH, SCREEN_HEIGHT))
   source_pos, target_pos = base_objects.tkinter_img_large(
       source, target)  # [x1,y1,x2,y2], [x1,y1]
   print("sourcepos", source_pos)
   print("target_pos", target_pos)
   if not source_pos:
      raise Exception('tkinter did not receive source image from user')

   source = source.crop(source_pos)
   print(f"working with source shape : ", source.size)
   source = np.asarray(source)
   m, n = source.shape[:2]
   source_dict = {'Reds': source[::, ::, 0],
                  'Greens': source[::, ::, 1], 'Blues': source[::, ::, 2]}

   #make target rectangle of the same size as source

   target_x, target_y = target_pos
   target = target.crop((target_x, target_y, target_x+n, target_y+m))
   target = np.asarray(target)
   target_dict = {'Reds': target[::, ::, 0],
                  'Greens': target[::, ::, 1], 'Blues': target[::, ::, 2]}

   #testing with just the grey version #[0.2989, 0.5870, 0.1140]
   axes[0].imshow(source, vmin=0, vmax=255)
   axes[1].imshow(target, vmin=0, vmax=255)
   #testing with all three versions

   final_arr = np.empty(shape=(m, n, 3))
   A = base_objects.lapAfinal2(m, n)
   for i, c in enumerate(source_dict.keys()):
      source = source_dict[c]
      target = target_dict[c]
      source = source.flatten()
      target = target.flatten()

      b = base_objects.make_b_min(m, n, source, target)
      print(f"A.shape", A.shape)
      print(f"b.shape", b.shape)
      x = sc.linalg.spsolve(A, b)

      print("before glueing", x.shape)
      x = base_objects.rebuild_u(x, target.flatten(), m, n)
      print("after glueing", x.shape)
      x[x < 0] = 0
      x[x > 255] = 255
      axes[i+2].imshow(x.astype('uint8'), cmap=c, vmin=0, vmax=255)
      final_arr[::, ::, i] = x
   final_arr = final_arr.astype('uint8')

   final_img = Image.fromarray(final_arr)
   target = Image.open(target_path).resize((SCREEN_WIDTH, SCREEN_HEIGHT))
   target.paste(final_img, (target_x, target_y))
   target.show()
   axes[5].imshow(target)

