#!/usr/bin/env python3

import argparse
import logging
import os
import sys

logging.basicConfig(level=logging.INFO)

MY_PATH = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(MY_PATH, 'python')))

import tmxlite

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def printTmxMapInfo(filename : str):
    map = tmxlite.TmxMap()
    map.load(filename)
    print(f"Map version: {map.getVersion()}")
    if map.isInfinite():
        print("Map is infinite.\n")
    mapProperties = map.getProperties()
    print(f"Map has {mapProperties.size()} properties")
    for prop in mapProperties:
        print(f"Found property: \"{prop.getName()}\", Type: {prop.getTypeName()}")
    layers = map.getLayers()
    print(f"Map has {layers.size()} layers")
    for layer in layers:
        print(f"Found Layer: \"{layer.getName()}\", Type: {layer.getTypeName()}")

        if layer.getType() == tmxlite.TmxLayerType.Group:
            sublayers = layer.getLayers()
            print(f"LayerGroup has {sublayers.size()} sublayers")
            for sublayer in sublayers:
                print(f"Found Sublayer: \"{sublayer.getName()}\", Type: {sublayer.getTypeName()}")
                if sublayer.getType() == tmxlite.TmxLayerType.Tile:
                    tiles = sublayer.getTiles()
                    if tiles:
                        print(f"TileLayer has {tiles.size()} tiles")
                    chunks = sublayer.getChunks()
                    if chunks:
                        print(f"TileLayer has {chunks.size()} chunks")
                    tilesProperties = sublayer.getProperties()
                    if tilesProperties:
                        print(f"TileLayer has {tilesProperties.size()} properties")
                        for prop in tilesProperties:
                            print(f"Found property: \"{prop.getName()}\", Type: {prop.getTypeName()}")

        elif layer.getType() == tmxlite.TmxLayerType.Object:
            objects = layer.getObjects()
            print(f"Found has {objects.size()} objects in layer")
            for object in objects:
                print(f"Object {object.getUID()}, Name: \"{object.getName()}\"")
                objProperties = object.getProperties()
                if objProperties:
                    print(f"Object has {objProperties.size()} properties")
                    for prop in objProperties:
                        print(f"Found property: \"{prop.getName()}\", Type: {prop.getTypeName()}")

        elif layer.getType() == tmxlite.TmxLayerType.Image:
            print(f"ImagePath: \"{layer.getImagePath()}\"")

        elif layer.getType() == tmxlite.TmxLayerType.Tile:
            tiles = layer.getTiles()
            if tiles:
                print(f"TileLayer has {tiles.size()} tiles")
            chunks = layer.getChunks()
            if chunks:
                print(f"TileLayer has {chunks.size()} chunks")
            tilesProperties = layer.getProperties()
            if tilesProperties:
                print(f"TileLayer has {tilesProperties.size()} properties")
                for prop in tilesProperties:
                    print(f"Found property: \"{prop.getName()}\", Type: {prop.getTypeName()}")

    tilesets = map.getTilesets()
    print(f"Map has {tilesets.size()} tilesets")
    for tileset in tilesets:
        print(f"Found Tileset \"{tileset.getName()}\", {tileset.getFirstGID()} - {tileset.getLastGID()}")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def loadTmxMap(filename : str):
    map = tmxlite.TmxMap(filename)
    map_rows, map_cols = map.getTileCount()
    print(f"Map dimensions: {map_rows} x {map_cols}")
    tile_width, tile_height = map.getTileSize()
    print(f"Tile size: {tile_width} x {tile_height}")
    tilesets = map.getTilesets()
    print(f"Map has {tilesets.size()} tilesets")
    for tileset in tilesets:
        twidth, theight = tileset.getTileSize()
        iwidth, iheight = tileset.getImageSize()
        print(f"- Tileset \"{tileset.getName()}\" ({tileset.getFirstGID()}-{tileset.getLastGID()}): Image=\"{tileset.getImagePath()}\" ({iwidth}x{iheight}), Tile Size={twidth}x{theight}")
        for tile in tileset.getTiles():
            tidx = tile.getTerrainIndices()
            #~ print(f"{tile.getID()} {tile.getImagePath()} {tile.getImagePosition()} {tile.getImageSize()} {[i for i in tidx]}")

    layers = map.getLayers()
    print(f"Map has {layers.size()} layers")
    for layer in layers:
        if layer.getType() != tmxlite.TmxLayerType.Tile:
            continue
        tiles = layer.getTiles()
        print(f"- Layer \"{layer.getName()}\" ({layer.getTypeName()}) has {tiles.size()} tiles")

        for y in range(map_rows):
            for x in range(map_cols):
                tile_index = x + (y * map_cols)
                cur_gid = tiles[tile_index].getID();
                if not cur_gid:
                    continue
                for tileset in tilesets:
                    if tileset.getFirstGID() <= cur_gid and tileset.getLastGID() >= cur_gid:
                        print(f"  [{x}, {y}]: {cur_gid} -> Tileset \"{tileset.getName()}\" ({tileset.getFirstGID()}-{tileset.getLastGID()})")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--quiet", help="set logging to ERROR",
                        action="store_const", dest="loglevel",
                        const=logging.ERROR, default=logging.INFO)
    parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                        action="store_const", dest="loglevel",
                        const=logging.DEBUG, default=logging.INFO)
    parser.add_argument("-t", "--test", dest="test", required=False, help="Test to run", default=None)
    args = parser.parse_args()

    if args.test is None:
        tests = [ 'printtmx', 'loadtmx' ]
    else:
        tests = [ args.test ]

    for test in tests:
        logging.info(f"Running test: {test}")
        if test == 'printtmx':
            printTmxMapInfo("testdata/orthogonal-outside.tmx")
        if test == 'loadtmx':
            loadTmxMap("testdata/orthogonal-outside.tmx")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

if __name__ == "__main__":
    main()
