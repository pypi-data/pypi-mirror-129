# Flyr
![A picture of a FLIR thermogram, the embedded optical data and a Flyr render concatenated into one](https://bitbucket.org/nimmerwoner/flyr/downloads/readme_intro.jpg)

Flyr is a library for extracting thermal data from FLIR images written fully in Python, without depending on ExifTool.

Other solutions are wrappers around ExifTool to actually do the hard part of extracting the thermal data. Flyr is a reimplementation of the ExifTool's FLIR parser. Practically, this offers the following benefits:

* Faster decoding because no new process needs to be started and in-memory data does not need to be communicated to this other process
* More accurate, because Flyr uses all of the metadata to translate the raw values into Kelvin, while other projects have a certain set hardcoded. The differences are often about 0.1°C, but can be as high as 0.6°C.
* Easier and robust installation and deployment, because `flyr` is completely installable from PyPI.
* Arguably simpler use: no need to create a superfluous extraction object; simply call `thermogram = flyr.unpack(flir_file_path)` and done
* Extra features (see feature section) such as different units, built-in rendering and adjustable thermal data.

## Installation

Flyr is installable from [PyPi](https://pypi.org/project/flyr/): `pip install flyr`.

Flyr depends on three external packages, all installable through pip: `pip install numpy nptyping pillow`. Pillow does the conversion from embedded images to numpy arrays, nptyping allows for high quality array type annotations. Numpy provides the n-dimensional arrays necessary to contain the thermal and optical data.

## Usage and features
### Different units
Thermal data is available in kelvin, celsius and fahrenheit.

```python
import flyr

flir_path = "thermograms/flir_e5_2.jpg"
thermogram = flyr.unpack(flir_path)

thermal = thermogram.kelvin  # As kelvin
thermal = thermogram.celsius  # As celsius
thermal = thermogram.fahrenheit  # As fahrenheit
```

### Optical data can be read
![The optical photo embedded in the FLIR thermogram](https://bitbucket.org/nimmerwoner/flyr/downloads/readme_optical.jpg)

To read the embedded photo, access either `optical` or `optical_pil` to respectively get a 3D numpy or Pillow Image object with the photo.

```python

import flyr

flir_path = "thermograms/flir_e5_2.jpg"
thermogram = flyr.unpack(flir_path)
img_arr = thermogram.optical  # Also works
thermogram.optical_pil.save("optical.jpg")
```

### Built-in support for rendering
![Examples of different RGB renders of the same thermogram](https://bitbucket.org/nimmerwoner/flyr/downloads/readme_render_example.png)

Flyr has built-in support to render thermal data to RGB images. It is possible to use different [palettes](flyr/palettes) and normalize by percentiles or absolute values.

```python
import flyr

flir_path = "thermograms/flir_e5_2.jpg"
thermogram = flyr.unpack(flir_path)

palettes = ["turbo", "cividis", "inferno", "grayscale", "hot"]
for p in palettes:
    # The below call returns a Pillow Image object.
    # A sibling method called `render` returns a numpy array.
    render = thermogram.render_pil(
        min_v=27.1,
        max_v=35.6,
        unit="celsius",
        mode="minmax",
        palette=p,
    )
    render.save(f"render-{p}.png")
```

To render by percentiles, call as below. This approach is useful when it isn't know what temperature range to render.

```python
thermogram.render_pil(
    min_v=0.0,
    max_v=1.0,
    mode="percentilea",
    palette="copper",
).save(f"render-percentiles.png")
```

### Adjustable camera settings
![Examples of different RGB renders of the same thermogram](https://bitbucket.org/nimmerwoner/flyr/downloads/readme_render_emissivities.png)

It is possible to update the camera settings / parameters with which the thermal data is calculated. A typical value to adjust would be `emissivity`, but `object_distance`, `relative_humidity` and others are also configurable. See the parameters of [`FlyrThermogam.__raw_to_kelvin()`](https://bitbucket.org/nimmerwoner/flyr/src/90635d825bba132a99a240c511df892fab1f05bb/flyr/thermogram.py#lines-217) for which.

```python
import flyr

flir_path = "thermograms/flir_e5_2.jpg"
thermogram = flyr.unpack(flir_path)

emissivities = [0.6, 0.7, 0.8, 0.9, 1.0]
for e in emissivities:
    thermogram = thermogram.adjust_metadata(emissivity=e)
    # thermal = thermogram.celsius  # Access updated data as normal
	render = thermogram.render_pil(
        min_v=27.1,
        max_v=35.6,
        unit="celsius",
        mode="minmax",
        palette="viridis",
    )
	render.save(f"render-{e}.png")
```

### Read from file, from file handle or binary stream
Call `flyr.unpack` on a filepath to receive a numpy array with the thermal data. Alternatively, first open the file in binary mode for reading and and pass the the file handle to `flyr.unpack`.

```python
import flyr

# From file path
flir_path = "thermograms/flir_e5_2.jpg"
thermogram = flyr.unpack(flir_path)  # From file path

# From file handle / binary stream
with open(flir_path, "rb") as flir_handle:  # In binary mode!
	thermogram = flyr.unpack(flir_handle)
```

## Supported cameras
Currently this library has been tested to work with:

* FLIR E4
* FLIR E5
* FLIR E6
* FLIR E8
* FLIR E8XT
* FLIR E53
* FLIR P60 (PAL)
* FLIR E75
* FLIR T630SC
* FLIR T660

However, the library is still in an early phase and lacks robust handling of inconsistent files. When it encounters such an image it immediately gives up raising a ValueError, while it could also do a best effort attempt to extract anyway. This is planned.

Camera's that sometimes do and don't work:

* FLIR ThermaCAM P640
* FLIR ThermaCAM P660 West (more often doesn't than does)

Camera's found not to work (yet):

* FLIR E60BX
* FLIR ThermoCAM B400
* FLIR ThermaCAM SC640
* FLIR ThermaCam SC660 WES
* FLIR ThermaCAM T-400
* FLIR S60 NTSC
* FLIR SC620 Western
* FLIR T400 (Western)
* FLIR T640
* FLIR P660

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Most help is currently needed supporting more models and testing against more pictures. Testing and developing for your own camera's images or FLIR Tools' samples is recommended.

## Acknowledgements
This code would not be possible without [ExifTool](https://exiftool.org/)'s efforts to [document](https://exiftool.org/TagNames/FLIR.html) the FLIR format.
[Previous work](https://github.com/Nervengift/read_thermal.py) in Python must
also be acknowledged for creating a workable solution.

## License
Flyr is licensed under The European Union Public License 1.2. The English version is included in the license file. Translations for all EU languages, each fully legally valid, can be found at the [EUPL](https://eupl.eu/) website.
