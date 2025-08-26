import { Link, Outlet } from 'react-router-dom'

export function Layout() {
	return (
		<div style={{ fontFamily: 'system-ui, sans-serif', maxWidth: 920, margin: '0 auto', padding: 16 }}>
			<header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
				<h1>Donation Matcher</h1>
				<nav style={{ display: 'flex', gap: 12 }}>
					<Link to="/">Home</Link>
					<Link to="/register">Register Donor</Link>
					<Link to="/match">Find Match</Link>
				</nav>
			</header>
			<Outlet />
		</div>
	)
}