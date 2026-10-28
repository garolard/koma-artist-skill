# KOMA Artist Skills

Three portable Agent Skills for artists using AI in their workflow:

- **koma-artist-review** proposes a set from a collection of artwork.
- **koma-artist-plan** develops a set interactively with the artist.
- **koma-artist-prepare** makes a folder of copies for Studio bulk import and a checklist for the remaining decisions.

## Install

Once this repository is public, use a supported Agent Skills installer with its GitHub repository URL, for example:

```sh
npx skills add <owner>/<repository>
```

Choose the skills and agents in the installer. Agent support, invocation syntax, image access, and ability to write local files vary. Ask for a KOMA review, plan, or preparation in plain language if your agent does not expose named commands. These names follow the portable skill format; `koma-assistant:review`-style commands are not assumed to exist in every harness.

The skill does not upload, submit, or automatically assign Studio metadata. Images imported into a fresh draft fill empty slots in filename order; review framing and assign rarities in Studio. Keep the panel folder separate from the cover and checklist.

## Maintaining KOMA rules

Each skill includes its own reference files so it remains self-contained when installed individually. Update all three copies together when KOMA changes. The KOMA app and Studio remain authoritative; the included reference was checked on 2026-10-28.

## Preparing panel files

The prepare skill includes a Python 3 helper that copies approved artwork into a new, numbered panel folder without modifying the originals. The agent can create its JSON input from an approved plan; see [the preparation plan format](skills/koma-artist-prepare/references/prepare-plan.md). The helper targets a fresh, empty Studio draft; shape, framing, rarity, cover and previews still need attention in Studio.
