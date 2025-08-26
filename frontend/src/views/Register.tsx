import { FormEvent, useState } from 'react'
import axios from 'axios'

const API_URL = (import.meta as any).env.VITE_API_URL || 'http://localhost:8000'

export function Register() {
	const [status, setStatus] = useState<string | null>(null)
	const [loading, setLoading] = useState(false)

	async function onSubmit(e: FormEvent<HTMLFormElement>) {
		e.preventDefault()
		setStatus(null)
		setLoading(true)
		const form = new FormData(e.currentTarget)
		const payload = Object.fromEntries(form.entries()) as any
		payload.latitude = parseFloat(payload.latitude)
		payload.longitude = parseFloat(payload.longitude)
		payload.is_active = true
		try {
			await axios.post(`${API_URL}/donors/register`, payload)
			setStatus('Registered successfully')
			e.currentTarget.reset()
		} catch (err: any) {
			setStatus(err?.response?.data?.detail || 'Registration failed')
		} finally {
			setLoading(false)
		}
	}

	return (
		<form onSubmit={onSubmit} style={{ display: 'grid', gap: 8, maxWidth: 560 }}>
			<input name="full_name" placeholder="Full name" required />
			<input name="email" placeholder="Email (optional)" />
			<input name="phone" placeholder="Phone (optional)" />
			<select name="blood_group" required>
				<option value="">Blood group</option>
				<option>A</option>
				<option>B</option>
				<option>AB</option>
				<option>O</option>
			</select>
			<select name="rh_factor" required>
				<option value="">Rh factor</option>
				<option value="+">+</option>
				<option value="-">-</option>
			</select>
			<input name="latitude" placeholder="Latitude" required type="number" step="any" />
			<input name="longitude" placeholder="Longitude" required type="number" step="any" />
			<input name="city" placeholder="City" />
			<input name="country" placeholder="Country" />
			<input name="available_organs" placeholder="Available: e.g., blood,kidney" />
			<button disabled={loading} type="submit">{loading ? 'Saving...' : 'Register'}</button>
			{status && <p>{status}</p>}
		</form>
	)
}