# GURPS sheet source layout

This folder holds the source assets used to generate the final Roll20 sheet files in the parent directory.

## Current mode

The build script is intentionally baseline-safe: it reads the existing committed final files and verifies that the generated output still matches them exactly before the sheet is split into partials.

## Planned structure

- `html/` for shared page sections and sheet templates
- `css/` for modular stylesheet sections
- `js/` for worker logic and support modules
- `build.js` to concatenate and validate the generated output
- `manifest.json` to declare source ordering for each generated file

Once the source tree is populated, run:

- `npm run build:check` to verify the generated output still matches the committed files.
- `npm run build` to regenerate the final outputs.
- `npm run lint` to catch JavaScript issues before upload.
