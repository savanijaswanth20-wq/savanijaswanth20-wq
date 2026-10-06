# Profile design

The editorial layout uses original SVG code and artwork, inspired by the section
structure and dark blue visual direction of [Ug0510's profile](https://github.com/Ug0510/Ug0510).
It uses Jaswanth's own photo, projects, experience and public GitHub metrics.

## Regenerate the design

Run the following from this repository. No dependencies are required.

```sh
python3 scripts/build_editorial.py
GITHUB_REPOSITORY_OWNER=savanijaswanth20-wq python3 scripts/update_profile.py
```

The second command fetches the current public metrics. The scheduled workflow
also refreshes both builder dashboards and the README metrics.

Edit the text and layout in `scripts/build_editorial.py`. All editorial panels
have a separate mobile layout. Their CSS animations stop when the viewer requests
reduced motion, and their content remains visible without animation. GitHub's
Markdown supports animated images; it does not run JavaScript or background audio.
Clickable project and contact links are placed in the README around or below the
images because SVG images cannot contain interactive controls on GitHub.

## Sources

- `assets/profile-avatar.jpg` is the unchanged public photo from Jaswanth's GitHub
  avatar, fetched on 6 October 2026.
- Display lettering is Barlow Condensed Bold by Jeremy Tribby, converted to SVG
  glyph outlines. Source: https://github.com/google/fonts/tree/main/ofl/barlowcondensed
- The font is distributed under the SIL Open Font License 1.1. Its copyright and
  license are retained in `assets/editorial-source/OFL-BarlowCondensed.txt`.
- Existing 3D animation, résumé and contribution assets remain available.
