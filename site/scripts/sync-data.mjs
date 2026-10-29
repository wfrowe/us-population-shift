// Copies ../data/processed into public/data so the website can load the files.
// Runs automatically before `npm run dev` and `npm run build`.
// public/data is a copy and is git-ignored; the real files live in data/processed.
import { cpSync, existsSync, mkdirSync, rmSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const source = fileURLToPath(new URL('../../data/processed', import.meta.url));
const target = fileURLToPath(new URL('../public/data', import.meta.url));

if (!existsSync(source)) {
	console.error(`No processed data found at ${source}. Run the Python step first.`);
	process.exit(1);
}

rmSync(target, { recursive: true, force: true });
mkdirSync(target, { recursive: true });
cpSync(source, target, { recursive: true });
console.log(`Copied data/processed -> site/public/data`);
