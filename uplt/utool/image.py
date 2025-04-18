import numpy as np
from numpy import ndarray


def image_range(image: ndarray) -> int | float:
    """
    Guess the range by an image type and values
    """
    # int image
    if image.dtype.type == np.uint8:
        return 255

    if image.dtype.type == np.uint16:
        return 65535

    # float image
    max_value = np.max(image)

    if max_value < 1.01:
        return 1.0

    if max_value < 255:
        return 255

    if max_value < 65535:
        return 65535

    raise RuntimeError('image range detection failure')


def image_encode_base64(image: ndarray, value_range: float) -> str:
    import base64
    from io import BytesIO
    from PIL import Image

    image_u8 = (255 * (image / value_range)).astype(np.uint8)

    pil_image = Image.fromarray(image_u8)
    prefix = 'data:image/png;base64,'

    with BytesIO() as stream:
        pil_image.save(stream, format='png')
        image_base64 = prefix + base64.b64encode(stream.getvalue()).decode('utf-8')

    return image_base64