// The one place to set this project's name and summary.
// Everything else on the page is written in src/pages/index.astro.
export const project = {
	title: 'Where US population has grown since 2010',
	summary:
		'The US added 32.5 million people from 2010 to 2025. About half of that net gain went to five states: Texas, Florida, California, North Carolina and Georgia.',
};

// Set by the deploy workflow. Falls back to the GitHub profile when running locally.
export const repoUrl: string = import.meta.env.PUBLIC_REPO_URL ?? 'https://github.com/wfrowe';
