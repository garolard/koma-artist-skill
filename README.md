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
