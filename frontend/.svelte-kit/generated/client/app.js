export { matchers } from './matchers.js';

export const nodes = [
	() => import('./nodes/0'),
	() => import('./nodes/1'),
	() => import('./nodes/2'),
	() => import('./nodes/3'),
	() => import('./nodes/4'),
	() => import('./nodes/5'),
	() => import('./nodes/6'),
	() => import('./nodes/7'),
	() => import('./nodes/8'),
	() => import('./nodes/9'),
	() => import('./nodes/10'),
	() => import('./nodes/11'),
	() => import('./nodes/12'),
	() => import('./nodes/13'),
	() => import('./nodes/14'),
	() => import('./nodes/15'),
	() => import('./nodes/16'),
	() => import('./nodes/17'),
	() => import('./nodes/18'),
	() => import('./nodes/19'),
	() => import('./nodes/20'),
	() => import('./nodes/21'),
	() => import('./nodes/22'),
	() => import('./nodes/23'),
	() => import('./nodes/24'),
	() => import('./nodes/25'),
	() => import('./nodes/26'),
	() => import('./nodes/27'),
	() => import('./nodes/28'),
	() => import('./nodes/29'),
	() => import('./nodes/30'),
	() => import('./nodes/31'),
	() => import('./nodes/32'),
	() => import('./nodes/33'),
	() => import('./nodes/34'),
	() => import('./nodes/35'),
	() => import('./nodes/36'),
	() => import('./nodes/37'),
	() => import('./nodes/38')
];

export const server_loads = [];

export const dictionary = {
		"/(app)": [7,[2]],
		"/(app)/admin": [8,[2,3]],
		"/(app)/admin/evaluations": [9,[2,3]],
		"/(app)/admin/functions": [10,[2,3]],
		"/(app)/admin/functions/create": [11,[2,3]],
		"/(app)/admin/functions/edit": [12,[2,3]],
		"/(app)/admin/settings": [13,[2,3]],
		"/(app)/admin/users": [14,[2,3]],
		"/auth": [35],
		"/(app)/channels/[id]": [16,[2]],
		"/(app)/c/[id]": [15,[2]],
		"/error": [36],
		"/(app)/home": [17,[2,4]],
		"/(app)/playground": [18,[2,5]],
		"/(app)/playground/completions": [19,[2,5]],
		"/(app)/playground/notes": [20,[2,5]],
		"/s/[id]": [37],
		"/watch": [38],
		"/(app)/workspace": [21,[2,6]],
		"/(app)/workspace/functions/create": [22,[2,6]],
		"/(app)/workspace/knowledge": [23,[2,6]],
		"/(app)/workspace/knowledge/create": [25,[2,6]],
		"/(app)/workspace/knowledge/[id]": [24,[2,6]],
		"/(app)/workspace/models": [26,[2,6]],
		"/(app)/workspace/models/create": [27,[2,6]],
		"/(app)/workspace/models/edit": [28,[2,6]],
		"/(app)/workspace/prompts": [29,[2,6]],
		"/(app)/workspace/prompts/create": [30,[2,6]],
		"/(app)/workspace/prompts/edit": [31,[2,6]],
		"/(app)/workspace/tools": [32,[2,6]],
		"/(app)/workspace/tools/create": [33,[2,6]],
		"/(app)/workspace/tools/edit": [34,[2,6]]
	};

export const hooks = {
	handleError: (({ error }) => { console.error(error) }),
	
	reroute: (() => {}),
	transport: {}
};

export const decoders = Object.fromEntries(Object.entries(hooks.transport).map(([k, v]) => [k, v.decode]));

export const hash = false;

export const decode = (type, value) => decoders[type](value);

export { default as root } from '../root.svelte';