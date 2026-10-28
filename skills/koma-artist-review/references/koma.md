# KOMA set and Studio reference

Checked against KOMA specs on 2026-10-28. Confirm against the current KOMA documentation when available; report uncertainty if rules may have changed.

A standard-v1 set has 49 numbered panels: 24 common, 12 rare, 8 epic, 4 legendary, 1 unique. Titles are 1–60 characters after trimming. Set code is 2–8 uppercase ASCII letters or digits and must be unique. Choose one cover and exactly three distinct panel previews.

Full panel art sizes: 1x1 520x520; 2x1 1120x520; 1x2 520x1120; 3x1 1720x520; 2x2 1120x1120. Cover: 1024x1312. These are rendered art dimensions, not minimum input file dimensions. Studio accepts images the browser can decode and renders its own sizes. It warns if the cropped source has insufficient pixels.

Studio bulk import sorts filenames naturally, filling empty slots in ascending order, and derives titles from filenames only for untitled slots. It guesses shape if absent and auto-frames using a centered crop; framing starts unreviewed. It does not import rarity or the plan. Auto-shape considers 1x1, 2x1, 1x2, 3x1, not 2x2. Cover is handled separately. Check order and empty slots before import; review each framing, shape and rarity in Studio. Draft submission enters admin review; approval is not automatic.
