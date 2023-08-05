# hex_to_rgb()

## How to use

```python
from colorcodetools.hex.convert import HexToRgb
rgb_to_hex = HexToRgb()
rgb_to_hex.hex_to_rgb("#f2f2f2", True)
   ```

## Parameters

1. Required parameters:

   - hexcode:  
      Enter hex code which should be converted.
     - `type: string`
     - `default: None`
     - `example: '#f2f2f2'`

2. Optional parameters

   - prefix:  
     Decide if the converted rgbcode should have a 'rgb' respectively 'rgba' prefix.
     - `type: boolean`
     - `default: True`

## Return value

- `type: boolean or string`
