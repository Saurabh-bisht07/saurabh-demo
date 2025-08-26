import { RouteObject } from 'react-router-dom'
import { Layout } from './ui/Layout'
import { Home } from './views/Home'
import { Register } from './views/Register'
import { Match } from './views/Match'

export const routes: RouteObject[] = [
	{
		path: '/',
		element: <Layout />,
		children: [
			{ index: true, element: <Home /> },
			{ path: 'register', element: <Register /> },
			{ path: 'match', element: <Match /> },
		],
	},
]