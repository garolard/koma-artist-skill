# Preparation plan

The helper accepts a UTF-8 JSON file with a `panels` array in slot order and an optional `template` (`standard-v1`, `small-v1` or `mini-v1`; default `standard-v1`). Source paths are absolute or relative to the JSON file. Each entry has an integer `slot`, a `source` path and a `title` approved by the artist:

```json
{
  "template": "small-v1",
  "panels": [
    { "slot": 1, "source": "art/alley.png", "title": "Lantern Alley" },
    { "slot": 2, "source": "art/fox.jpg", "title": "Fox Mask" }
  ]
}
```

Run `python3 scripts/prepare.py plan.json output/panels` from the skill directory, or use the absolute path to the script. The output folder must not exist and its parent must exist. The script requires consecutive slots from 1 for a fresh draft, accepts up to the template's panel count (49 for standard-v1, 25 for small-v1, 16 for mini-v1), and rejects unknown templates and duplicate source files. It copies the bytes without transforming images. Titles must be 1–60 characters, must not start with a digit or separator, and cannot contain hyphens or underscores, because Studio's filename-to-title conversion would change them. It rejects path separators, control characters and common nonportable filename characters. Adjust titles in Studio if the intended title cannot be encoded this way. The script does not check browser image compatibility.

Only drag the output folder's image contents into a fresh Studio draft. Cover, shape, rarity, previews and framing are not transferred; Studio's guessed shape and centered framing must be reviewed. An incomplete list is allowed for a partial draft, but publishing requires all panels of the chosen template (49, 25 or 16).
