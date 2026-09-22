# Profile artwork source

The profile uses a custom, editable 3D scene created in Higgsfield 3D Jutsu, native Higgsedit typography, and self-contained SVG project cards.

## Files

- `scripts/build_scene.py`: Blender 5.2 source for the SVJ core, orbiting rings, floating API/AI/UI modules, materials, lights, animation and delivery camera. Run in Higgsfield 3D Jutsu, which provides the `artifacts` registry. This creates a four-second loop with matching poses at frames 1 and 49; exported playback uses 48 frames at 12 fps.
- `scripts/render_glb.cjs`: portable scene rendering with Three.js 0.180.0 and Playwright. Place the exported `scene.glb` in the working directory. Install `three@0.180.0` and `playwright`, then Chromium with `npx playwright install chromium`. Run the script to create PNG frames and `loop-check.json`.
- `scripts/render_banner.jsx`: native Higgsedit composition for the desktop and mobile banners. Put `core.mp4` in the working directory, then run `higgsedit build scripts/render_banner.jsx`. Montserrat is a built-in Higgsedit font. It exports both posters and MP4s.
- `scripts/build_cards.py`: standard-library Python generator for responsive, animated project SVGs. Run `python3 scripts/build_cards.py`.

Encode the scene frames with FFmpeg:

```sh
ffmpeg -framerate 12 -i frames/%03d.png -c:v libx264 -crf 17 -pix_fmt yuv420p core.mp4
```

Convert each finished banner MP4 into a looping GIF:

```sh
ffmpeg -i hero.mp4 -filter_complex '[0:v]split[a][b];[a]palettegen=max_colors=160:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle' -loop 0 hero.gif
```

## GitHub delivery

The README uses permanent Higgsfield media URLs for the rendered GIFs and PNG posters, and repository-relative paths for the SVG artwork. Replacing the animation requires updating the four header image URLs. The `<picture>` sources select a mobile composition or a still poster when reduced motion is requested. The SVG cards also respect reduced-motion settings.

The existing `Update profile` GitHub Actions workflow refreshes the contribution snake, public statistics, and profile links daily. Keep the `PROFILE-STATS` and `PROFILE-LINKS` comment markers intact when editing the README.

The Blender lighting preview and the portable GLB render use different renderers, so reflections can differ. Both use the same geometry, camera, materials and animation. The scene and typography are authored in code; they are not AI-generated footage.
