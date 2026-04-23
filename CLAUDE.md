# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A collection of FreeCAD Python macros that generate 3D-printable Monopoly board game pieces using the FreeCAD Part workbench API. All pieces are designed to interlock via peg-and-hole connectors.

## Running the Macros

Open FreeCAD, then run a macro via **Macro → Execute Macro** (or **Makro → Makro Çalıştır** in Turkish UI). Each macro creates a new FreeCAD document and saves a `.FCStd` file.

> **Note:** All macros hardcode `doc.saveAs("/home/user/...")`. Update the path to your actual home directory before running, or the save will fail.

## Piece Dimensions & Key Parameters

All values are in millimeters.

| Piece | File | Size |
|---|---|---|
| Property square | `monopoly_square_tile.FCMacro` | 40×40×4mm + 6mm color strip |
| Corner squares (GO, Jail, Free Parking, Go To Jail) | `monopoly_corner_tiles.FCMacro` | 60×60×4mm |
| House | `monopoly_buildings.FCMacro` | 8×8×10mm (6mm body + 4mm roof) |
| Hotel | `monopoly_buildings.FCMacro` | 12×8×11mm (flat roof + chimney) |
| Player tokens (6 types) | `monopoly_tokens.FCMacro` | ~15mm tall, 10mm base diameter |

## Interlocking System

Tiles connect to each other via a consistent peg-and-hole system defined in both `monopoly_square_tile.FCMacro` and `monopoly_corner_tiles.FCMacro`:

- **Peg:** `PEG_R = 1.0mm` radius, `PEG_H = 2.0mm` length — protrudes from left and right edges at mid-height
- **Hole:** `HOLE_R = 1.1mm` (0.1mm tolerance) — on front and back edges to accept pegs from adjacent tiles
- `WALL = 1.5mm` wall thickness used for hole depth calculation

## FreeCAD API Pattern

All macros follow the same structure:
1. `FreeCAD.newDocument(...)` — create document
2. Construct geometry with `Part.makeBox`, `Part.makeCylinder`, `Part.makeSphere`
3. Combine with `.fuse()` (union) and `.cut()` (subtraction)
4. `doc.addObject("Part::Feature", name)` + assign `.Shape`
5. Set `.ViewObject.ShapeColor` as an RGB tuple `(r, g, b)` with values 0.0–1.0
6. `doc.recompute()` then fit view
7. `doc.saveAs(path)` to persist

## Export for 3D Printing

The file `monopoly_square_tile-PropertySquare.3mf` is an example export. To export other pieces: in FreeCAD, select the shape object, then **File → Export** and choose `.3mf` or `.stl`.
