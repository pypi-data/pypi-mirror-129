# rgb_to_hex()

## How to use

```python
from colorcodetools.rgb.convert import RgbToHex
rgb_to_hex = RgbToHex()
rgb_to_hex.rgb_to_hex("(134, 128, 76)", 1.0, True)
   ```

## Parameters

1. Required parameters:

   - rgb:  
      Enter rgb code which should be converted.
     - `type: string`
     - `default: None`
     - `example: '(255, 255, 255)'`

2. Optional parameters

   - a:  
     Give an alpha value to the converter.

     - `type: float`
     - `default: 1.0`
     - `example: 0.5`

   - prefix:  
     Decide if the converted rgbcode should have a 'rgb' respectively 'rgba' prefix.
     - `type: boolean`
     - `default: True`

## Return value

- `type: boolean or string`
