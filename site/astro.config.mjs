// @ts-check
import { defineConfig } from 'astro/config';

// Project site: served at https://wfrowe.github.io/<repo-name>/
// The deploy workflow sets BASE_PATH from the repo name, so nothing here needs
// editing when you start a project from this template. Locally it is "/".
export default defineConfig({
	site: 'https://wfrowe.github.io',
	base: process.env.BASE_PATH ?? '/',
});
