import { FormEvent, useState } from 'react'
import axios from 'axios'

const API_URL = (import.meta as any).env.VITE_API_URL || 'http://localhost:8000'

type Donor = {
	id: number
	full_name: string
	email?: string
	phone?: string
	blood_group: string
	rh_factor: string
	city?: string
	country?: string
	distance_km?: number
	reliability_score?: number
}

export function Match() {
	const [results, setResults] = useState<Donor[]>([])
	const [status, setStatus] = useState<string | null>(null)
	const [loading, setLoading] = useState(false)

	async function onSubmit(e: FormEvent<HTMLFormElement>) {
		e.preventDefault()
		setStatus(null)
		setLoading(true)
		const form = new FormData(e.currentTarget)
		const payload: any = Object.fromEntries(form.entries())
		payload.latitude = parseFloat(payload.latitude)
		payload.longitude = parseFloat(payload.longitude)
		payload.max_km = parseFloat(payload.max_km)
		payload.limit = parseInt(payload.limit, 10)
		try {
			const { data } = await axios.post(`${API_URL}/match/search`, payload)
			setResults(data)
			setStatus(`${data.length} donors found`)
		} catch (err: any) {
			setStatus(err?.response?.data?.detail || 'Search failed')
		} finally {
			setLoading(false)
		}
	}

	return (
		<div>
			<form onSubmit={onSubmit} style={{ display: 'grid', gap: 8, maxWidth: 640, marginBottom: 16 }}>
				<select name="patient_blood_group" required>
					<option value="">Patient Blood Group</option>
					<option>A</option>
					<option>B</option>
					<option>AB</option>
					<option>O</option>
				</select>
				<select name="patient_rh_factor" required>
					<option value="">Rh</option>
					<option value="+">+</option>
					<option value="-">-</option>
				</select>
				<input name="latitude" placeholder="Patient Latitude" required type="number" step="any" />
				<input name="longitude" placeholder="Patient Longitude" required type="number" step="any" />
				<input name="organ" placeholder="Organ (optional), e.g., blood" />
				<input name="max_km" placeholder="Max distance (km)" type="number" step="any" defaultValue="50" />
				<input name="limit" placeholder="Max results" type="number" defaultValue="20" />
				<button disabled={loading} type="submit">{loading ? 'Searching...' : 'Search'}</button>
			</form>
			{status && <p>{status}</p>}
			<ul style={{ display: 'grid', gap: 8, listStyle: 'none', padding: 0 }}>
				{results.map(d => (
					<li key={d.id} style={{ border: '1px solid #ddd', borderRadius: 8, padding: 12 }}>
						<div style={{ fontWeight: 600 }}>{d.full_name}</div>
						<div>{d.blood_group}{d.rh_factor} · {d.city || ''} {d.country || ''}</div>
						<div>Distance: {d.distance_km?.toFixed(1)} km · Reliability: {(d.reliability_score ?? 0).toFixed(2)}</div>
						<div>Contact: {d.phone || 'n/a'} {d.email ? `· ${d.email}` : ''}</div>
					</li>
				))}
			</ul>
		</div>
	)
}