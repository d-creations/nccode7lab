# Changelog

All notable changes to this project will be documented in this file.

## [1.0.5] - 2026-08-02

### Changed
- **USB Transfer — Source Extensions**: Pulled programs now retain their original USB file extension instead of always using the configured channel default.
- **USB Transfer — Multichannel Pulls**: Combined pulls now support programs found across any configured channel combination, including P3.
- **Transfer Panel — Simplified Actions**: Program rows now provide one Pull action with channel-specific Compare actions, and pushing is limited to the currently open file.

## [1.0.4] - 2026-07-30

### Changed
- **USB Transfer — Main and Subprogram Extensions**: Added machine-configured `.M` support for P1/main programs and `.S` support for P2/subprograms when listing, pulling, comparing, and pushing programs.
- **Transfer Panel — Channel Labels**: Transfer actions now show the CNC channel before its configured file convention, such as `P1 Main (.M)`, `P2 Sub (.S)`, and `P2 (.p-2)`.
- **USB Transfer — Channel Filtering**: Programs with the same O-number but different channel extensions are now kept separate and pulled from the selected channel.

## [1.0.3] - 2026-07-28

### Changed
- **NC Code Editor — Comment Colours (Light Theme)**: Parenthesis comments `(...)` in the GitHub light theme are now rendered in `#6a737d` instead of the near-invisible `#998` default.
- **NC Code Editor — Block-Skip Lines (Light Theme)**: Lines starting with `/` (block-skip modifier) are now highlighted in blue (`#0550ae`) to distinguish them from regular comments.
- **NC Code Editor — Comment Colours (Dark Theme)**: Comments in the One Dark theme are now brighter (`#848da0` vs. default `#5c6370`) for better readability, with block-skip lines shown in `#61afef`.

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
