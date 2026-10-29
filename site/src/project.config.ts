// The one place to set this project's name and summary.
// Everything else on the page is written in src/pages/index.astro.
export const project = {
	title: 'Project title',
	summary: 'One plain sentence on the question and what you found.',
};

// Set by the deploy workflow. Falls back to the GitHub profile when running locally.
export const repoUrl: string = import.meta.env.PUBLIC_REPO_URL ?? 'https://github.com/wfrowe';
