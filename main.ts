// Entry program for the gta6-meme-x-01 bounty.
//
// The whole entry is the X post itself; this program has exactly one job:
// take the POST.json that sits at the repository root and place a copy of
// it in the output directory, where the grader looks for it.
//
// Locations come from the environment when the grader provides them:
//   MAKEFUN_BOT_DIR    - directory holding POST.json (default /bot)
//   MAKEFUN_OUTPUT_DIR - directory that receives the copy (default /output)

import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { join } from "node:path";

const sourceDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const targetDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const sourceFile = join(sourceDir, "POST.json");
const targetFile = join(targetDir, "POST.json");

if (!existsSync(sourceFile)) {
  console.error(`error: POST.json not found at ${sourceFile}`);
  process.exit(1);
}

try {
  mkdirSync(targetDir, { recursive: true });
  copyFileSync(sourceFile, targetFile);
} catch (err) {
  console.error(
    `error: could not copy ${sourceFile} to ${targetFile}: ${(err as Error).message}`,
  );
  process.exit(1);
}

const bytes = statSync(targetFile).size;
console.log(`POST.json copied (${bytes} bytes)`);
