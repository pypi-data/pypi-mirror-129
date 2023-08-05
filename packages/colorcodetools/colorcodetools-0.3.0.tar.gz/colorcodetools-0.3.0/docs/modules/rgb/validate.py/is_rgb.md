# is_rgb()

## How to use

1. ```python
   from colorcodetools.rgb.validate import is_rgb
   is_rgb('(r, g, b)')
   ```
2. ```python
   import colorcodetools
   colorcodetools.rgb.validate.is_rgb('(r, g, b)')
   ```

## Parameters

1. Required parameters:

   - rgb:  
      Enter rgb code which should be inverted.
     - `type: string`
     - `default: None`
     - `example: '(255, 255, 255)'`

2. Optional parameters

   - a:  
     Give an alpha value to the inverter.

     - `type: float`
     - `default: 1.0`
     - `example: 0.5`

## Return value

- `type: boolean`
