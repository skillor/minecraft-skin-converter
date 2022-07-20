import cv2
import numpy as np

# Conversion instructions (x, y, w, h)
CI = [
    [55, 16, 1, 32],  # right arm, last column, back
    [51, 16, 1, 4],  # right arm, last column, bottom, main layer
    [51, 32, 1, 4],  # right arm, last column, bottom, second layer
    [47, 16, 8, 32],  # right arm, big middle region
    [63, 48, 1, 16],  # left arm, last column, back, second layer
    [59, 48, 1, 4],  # left arm, last column, bottom, second layer
    [55, 48, 8, 16],  # left arm, big middle region, second layer
    [47, 48, 1, 16],  # left arm, last column, back, main layer
    [43, 48, 1, 4],  # left arm, last column, bottom, main layer
    [39, 48, 8, 16]  # left arm, big middle region, main layer
]

# Arm FBLR regions (x, y, w, h)
FBLR = [
    [40, 20, 16, 12],  # right arm, main layer
    [40, 36, 16, 12],  # right arm, second layer
    [32, 52, 16, 12],  # left arm, main layer
    [48, 52, 16, 12]  # left arm, second layer
]

# Arm top & bottom regions (x, y, w, h)
TB = [
    [44, 16, 8, 4],  # right arm, main layer
    [44, 32, 8, 4],  # right arm, second layer
    [36, 48, 8, 4],  # left arm, main layer
    [52, 48, 8, 4]  # left arm, second layer
]

# Arm front & back regions (x, y, w, h, isBack)
FB = [
    [52, 20, 4, 12, True],  # right arm, main layer, back
    [44, 20, 4, 12, False],  # right arm, main layer, front
    [52, 36, 4, 12, True],  # right arm, second layer, back
    [44, 36, 4, 12, False],  # right arm, second layer, front
    [44, 52, 4, 12, True],  # left arm, main layer, back
    [36, 52, 4, 12, False],  # left arm, main layer, front
    [60, 52, 4, 12, True],  # left arm, second layer, back
    [52, 52, 4, 12, False]  # left arm, second layer, front
]

# Half to Full Conversion (sw, sh, sx, sy, dx, dy) must be mirrored horizontally
HTF = [
    [4, 4, 4, 16, 20, 48],
    [4, 4, 8, 16, 24, 48],
    [4, 12, 8, 20, 16, 52],
    [4, 12, 4, 20, 20, 52],
    [4, 12, 0, 20, 24, 52],
    [4, 12, 12, 20, 28, 52],
    [4, 4, 44, 16, 36, 48],
    [4, 4, 48, 16, 40, 48],
    [4, 12, 48, 20, 32, 52],
    [4, 12, 44, 20, 36, 52],
    [4, 12, 40, 20, 40, 52],
    [4, 12, 52, 20, 44, 52],
]


class SkinConverter:
    def _get_ratio_to_base(self):
        # get loaded image width to normal skin width (64) ratio
        h, w, c = self._image.shape
        return w / 64

    def _ratio_adjust(self, arr, ratio=-1):  # pixel region array, adjusted for skin ratio
        if ratio < 0:
            ratio = self._get_ratio_to_base()
        return list(map(lambda r: list(map(lambda e: e * ratio, r)), arr))

    def _clear_rect(self, x, y, w, h):
        x, y, w, h = int(x), int(y), int(w), int(h)
        self._image[y:y + h, x:x + w, :] = [0] * self._image.shape[2]

    def _draw_image(self, source_image, sx, sy, sw, sh, dx, dy, dw, dh, flip_horizontal=False):
        # draw from source image to destination
        sx, sy, sw, sh, dx, dy, dw, dh = int(sx), int(sy), int(sw), int(sh), int(dx), int(dy), int(dw), int(dh)
        roi = source_image[sy:sy + sh, sx:sx + sw]
        resized_roi = cv2.resize(roi, (dw, dh), interpolation=cv2.INTER_AREA)
        if flip_horizontal:
            resized_roi = cv2.flip(resized_roi, 1)
        self._image[dy:dy + dh, dx:dx + dw] = resized_roi

    def _move_rect(self, sx, sy, sw, sh, x, y, w=-1, h=-1, copy_mode=False, flip_horizontal=False):
        # move / stretch image region
        old_image = self._image.copy()
        if not copy_mode:
            self._clear_rect(sx, sy, sw, sh)
        w = sw if w < 0 else w
        h = sh if h < 0 else h
        self._draw_image(old_image, sx, sy, sw, sh, x, y, w, h, flip_horizontal=flip_horizontal)

    def _shift_rect(self, x, y, w, h, pixels_to_move, copy_mode=False):
        # shift rectangle of pixels on the x axis (use negative pixelsToMove to shift left)
        self._move_rect(x, y, w, h, x + pixels_to_move, y, -1, -1, copy_mode)

    def _is_empty_rect(self, x, y, w, h):
        x, y, w, h = int(x), int(y), int(w), int(h)
        return np.mean(self._image[y:y + h, x:x + w, 3]) == 0

    def _common_shift(self, ins, dx, dw, pixels_to_move, copy_mode=False, reverse_order=False):
        if reverse_order:
            pass
            ins = ins[::-1]  # using slice to work on a copy
        for v in ins:
            self._shift_rect(v[0] + dx, v[1], v[2] + dw, v[3], pixels_to_move, copy_mode)

    def __init__(self):
        self._image = None

    def set_image(self, image):
        self._image = image

    def get_image(self):
        return self._image.copy()

    def load_from_file(self, file_path):
        self.set_image(cv2.imread(file_path, cv2.IMREAD_UNCHANGED))

    def save_to_file(self, file_path):
        cv2.imwrite(file_path, self.get_image())

    def load_from_bytes(self, image_bytes):
        self.set_image(cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_UNCHANGED))

    def normalize_skin(self):
        if self.is_half_skin():
            self.half_to_full()

    def save_to_bytes(self):
        return cv2.imencode('.png', self.get_image())[1].tobytes()

    def is_half_skin(self):
        h, w, c = self._image.shape
        return w == h * 2 and self._get_ratio_to_base() % 1 == 0

    def is_full_skin(self):
        h, w, c = self._image.shape
        return w == h and self._get_ratio_to_base() % 1 == 0

    def is_valid_skin(self):
        return self.is_full_skin() or self.is_half_skin()

    def is_hd(self):
        return self._get_ratio_to_base() > 1

    def half_to_full(self):
        ratio = self._get_ratio_to_base()
        h, w, c = self._image.shape
        new_image = np.zeros((w, w, c), dtype=self._image.dtype)
        new_image[:h, :w] = self._image
        self._image = new_image
        for v in self._ratio_adjust(HTF, ratio):
            self._move_rect(v[2], v[3], v[0], v[1], v[4], v[5], copy_mode=True, flip_horizontal=True)

    def full_to_half(self):
        h, w, c = self._image.shape
        self._image = self._image[:int(h/2)]

    def is_steve(self):
        ratio = self._get_ratio_to_base()
        for v in self._ratio_adjust(FBLR + TB, ratio):
            if not self._is_empty_rect(v[0] + v[2] - ratio, v[1], ratio, v[3]):
                return True
        return False

    def steve_to_alex(self):
        self.steve_to_alex_squeeze()

    def alex_to_steve(self):
        self.alex_to_steve_stretch()

    def steve_to_alex_squeeze(self):  # convert Steve to Alex (squeeze)
        ratio = self._get_ratio_to_base()
        self._common_shift(CI, 0, 0, -ratio)

    def alex_to_steve_stretch(self):  # convert Alex to Steve (stretch)
        ratio = self._get_ratio_to_base()
        self._common_shift(CI, -2 * ratio, ratio, ratio, True, True)
