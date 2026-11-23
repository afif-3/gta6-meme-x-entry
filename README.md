[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/afif-3/gta6-meme-x-entry/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/afif-3/gta6-meme-x-entry/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

Entry for the [make.fun "Post a GTA 6 meme on X" bounty](https://make.fun/bounty/gta6-meme-x-01) ($500 in USDC).

# GTA 6 meme — entry for make.fun bounty gta6-meme-x-01

This repository is the hand-in for the make.fun bounty **"Post a GTA 6 meme
on X"** ($500, shared by the top 50). The entry itself is a single public
post on X: a GTA 6 meme whose picture carries the make.fun ghost mascot,
posted with a tag of @makefunai, a link to the bounty page, and the
entrant's play code in the text.

**The post:** https://x.com/Dgeatelafif/status/2124671560061714700

## What's in here

- `POST.json` — a one-field JSON object naming the post's address. This is
  the file the grader reads.
- `main.ts` — the entry program (Node 22, standard library only). All it
  does is copy `POST.json` from the repository root into the output
  directory.
- `make_meme.py` — a PIL script that renders the meme picture in code
  (neon Vice City sunset, skyline, palms, the ghost in sunglasses holding
  a fan of cash, and the caption). Its output, `meme.png`, is the same
  composition as the picture on the post.
- `meme.png` — the rendered 1200x1200 meme image.
- `LICENSE` — the repository license.

## How main.ts works

The program resolves two directories from the environment:

- `MAKEFUN_BOT_DIR` — where `POST.json` lives (default `/bot`)
- `MAKEFUN_OUTPUT_DIR` — where the copy goes (default `/output`)

It creates the output directory if needed, copies the file, and reports
how many bytes were copied. If `POST.json` is missing, or the copy fails,
it prints an error naming the paths involved and exits with status 1.

## Run it locally

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

After the run, `out/POST.json` is byte for byte the repository's
`POST.json`.

## Regenerate the meme picture

```sh
python3 make_meme.py
```

That rewrites `meme.png` next to the script.
