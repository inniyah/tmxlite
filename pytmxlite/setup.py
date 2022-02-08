#!/usr/bin/env python3

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

NAME = "tmxlite"
VERSION = "1.3.0"
DESCR = "A lightweight C++14 parsing library for tmx map files created with the Tiled map editor"
URL = "https://github.com/fallahn/tmxlite"
AUTHOR = "Matt Styles"
EMAIL = "matty_styles@hotmail.com"
LICENSE = "Zlib"
REQUIRES = ['cython']
PACKAGES = []

ext_modules=[
	Extension(
		name = "tmxlite",
		sources = [
			"./tmxlite.pyx",
			"../tmxlite/src/LayerGroup.cpp",
			"../tmxlite/src/Object.cpp",
			"../tmxlite/src/ImageLayer.cpp",
			"../tmxlite/src/ObjectGroup.cpp",
			"../tmxlite/src/ObjectTypes.cpp",
			"../tmxlite/src/Property.cpp",
			"../tmxlite/src/Tileset.cpp",
			"../tmxlite/src/Map.cpp",
			"../tmxlite/src/FreeFuncs.cpp",
			"../tmxlite/src/TileLayer.cpp",
			"../tmxlite/src/miniz.c",
			"../tmxlite/src/detail/pugixml.cpp",
		],
		libraries=[],
		include_dirs=["../tmxlite/include"],
		language='c++',
		extra_compile_args=[],
	)
]

if __name__ == "__main__":
	setup(
		name=NAME,
		version=VERSION,
		description=DESCR,
		author=AUTHOR,
		author_email=EMAIL,
		url=URL,
		license=LICENSE,
		packages=PACKAGES,
		install_requires=REQUIRES,
		zip_safe=False,
		cmdclass = {"build_ext": build_ext},
		ext_modules = ext_modules
	)
