# Changelog

All notable changes to this project will be documented in this file.

## [1.0.2] - 2026-07-28

### Changed
- **3D Toolpath Plot — Zoom to Fit on Plot**: Camera now automatically fits to the toolpath bounding box whenever a new plot is rendered.
- **3D Toolpath Plot — Reset View**: "Reset View" button now calls Zoom to Fit instead of a hardcoded camera position, falling back to the default position only when the scene is empty.
- **3D Toolpath Plot — Axis-Align Views (X-Y, X-Z, Y-Z)**: All axis-align view buttons now re-center the orbit target on the actual geometry before repositioning the camera, enabling consistent deep zoom after view alignment.

## [1.0.1] - 2026-06-24

### Added
- **Template Manager**: Introduced a new template manager to handle code snippets and blocks.
- **USB Transfer Protocol**: Added support for direct file and program transfer via USB connectivity.

### Changed
- **Siemens 840Di**: Updated and improved support for the Siemens 840Di control:
  - Fixed an issue where variables starting with axis letters (like `Z_POS`) would lose their assignments during sanitization.
  - Parameter parentheses `( )` such as those used in `CYCLE800` are now safely preserved instead of being stripped out as comments.
