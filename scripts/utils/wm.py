import cv2
from PIL import Image
import numpy as np
from imwatermark import WatermarkEncoder

def make_wm_encoder():
  print("Creating invisible watermark encoder (see https://github.com/ShieldMnt/invisible-watermark)...")
  wm = "SDV2"
  wm_encoder = WatermarkEncoder()
  wm_encoder.set_watermark('bytes', wm.encode('utf-8'))
  return wm_encoder

def put_watermark(img, wm_encoder=None):
  if wm_encoder is not None:
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    img = wm_encoder.encode(img, 'dwtDct')
    img = Image.fromarray(img[:, :, ::-1])
  img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
  img = Image.fromarray(img[:, :, ::-1])
  return img