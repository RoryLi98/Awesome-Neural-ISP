"""A minimal, readable classical ISP: RAW file -> sRGB PNG.

Every stage is a few lines of NumPy so the pipeline can be read top to bottom.
It is a teaching sketch, not a production ISP: no lens-shading correction,
no defect-pixel correction, no local tone mapping, and a plain global gamma.

    pip install rawpy colour-demosaicing imageio numpy
    python minimal_isp.py input.dng output.png
"""
import sys

import imageio.v3 as iio
import numpy as np
import rawpy
from colour_demosaicing import demosaicing_CFA_Bayer_Malvar2004

# CIE XYZ (D65) -> linear sRGB
XYZ_TO_SRGB = np.array([[3.2404542, -1.5371385, -0.4985314],
                        [-0.9692660, 1.8760108, 0.0415560],
                        [0.0556434, -0.2040259, 1.0572252]])


def run(path_in, path_out):
    raw = rawpy.imread(path_in)
    cfa = raw.raw_image_visible.astype(np.float64)
    colors = raw.raw_colors_visible                      # 0=R, 1=G, 2=B, 3=G2 at every pixel
    pattern = ''.join(chr(raw.color_desc[i]) for i in raw.raw_pattern.flatten())  # e.g. 'RGGB'

    # 1. Black level subtraction and normalization to [0, 1]
    black = np.array(raw.black_level_per_channel, dtype=np.float64)[colors]
    cfa = np.clip((cfa - black) / (raw.white_level - black), 0, 1)

    # 2. White balance: per-channel gains from the camera's as-shot estimate, applied on the mosaic
    wb = np.array(raw.camera_whitebalance, dtype=np.float64)
    if wb[3] == 0:
        wb[3] = wb[1]
    cfa = cfa * (wb / wb[1])[colors]

    # 3. Demosaicing (Malvar-He-Cutler 2004 linear interpolation)
    rgb_cam = demosaicing_CFA_Bayer_Malvar2004(np.clip(cfa, 0, 1), pattern)

    # 4. Color correction: camera RGB -> linear sRGB, built from the camera's XYZ->camera matrix
    cam_from_xyz = raw.rgb_xyz_matrix[:3, :]
    cam_from_srgb = cam_from_xyz @ np.linalg.inv(XYZ_TO_SRGB)
    cam_from_srgb /= cam_from_srgb.sum(axis=1, keepdims=True)  # keep white = white after WB
    srgb_lin = np.clip(rgb_cam @ np.linalg.inv(cam_from_srgb).T, 0, 1)

    # 5. Tone: simple global exposure so the 99th percentile maps to 1, then the sRGB transfer curve
    srgb_lin = np.clip(srgb_lin / max(np.percentile(srgb_lin, 99), 1e-6), 0, 1)
    srgb = np.where(srgb_lin <= 0.0031308, 12.92 * srgb_lin, 1.055 * srgb_lin ** (1 / 2.4) - 0.055)

    iio.imwrite(path_out, (srgb * 255 + 0.5).astype(np.uint8))


if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2])
