# invert_hex()

## How to use

1. ```python
   from colorcodetools.hex.invert import invert_hex
   invert_hex('hexcode')
   ```
2. ```python
   import colorcodetools
   colorcodetools.hex.invert.invert_hex('hexcode')
   ```

## Parameters

1. Required parameters:

   - hexcode:  
      Enter hex code which should be inverted. Supports also hex codes with alpha values.
     - `type: string`
     - `default: None`
     - `example: #f0f0f0`

2. Optional parameters
   - prefix:  
     Decide if the inverted hexcode should have a '#' prefix.
     - `type: boolean`
     - `default: True`

## Return value

- `type: boolean or string`
