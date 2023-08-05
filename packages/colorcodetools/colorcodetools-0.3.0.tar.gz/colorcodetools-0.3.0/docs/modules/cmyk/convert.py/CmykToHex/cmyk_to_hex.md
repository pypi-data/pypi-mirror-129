# cmyk_to_rgb()

## How to use

```python
from colorcodetools.cmyk.convert import CmykToHex
rgb_to_rgb = CmykToHex()
rgb_to_rgb.cmyk_to_hex('15/46/19/44', False)
   ```

## Parameters

1. Required parameters:

   - cmyk:  
      Enter cmyk code which should be converted.
     - `type: string`
     - `default: None`
     - `example: '15/46/19/44'`
     
2. Optional parameters

   - prefix:  
     Decide if the converted cmykcode should have a '#' prefix.
     - `type: boolean`
     - `default: True`

## Return value

- `type: boolean or string`
