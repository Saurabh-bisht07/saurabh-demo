import React, { useState } from 'react'
import { api } from '../lib/api'

const BLOOD_GROUPS = ['O-', 'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+']

export default function PatientSearch() {
  const [form, setForm] = useState({ blood_group: 'O+', latitude: '', longitude: '', donation_type: 'blood', organ: '' })
  const [results, setResults] = useState<any[]>([])
  const [message, setMessage] = useState('')

  const search = async (e: React.FormEvent) => {
    e.preventDefault()
    setMessage('')
    try {
      const params = new URLSearchParams({
        blood_group: form.blood_group,
        latitude: String(Number(form.latitude)),
        longitude: String(Number(form.longitude)),
        donation_type: form.donation_type,
        organ: form.organ,
        limit: '10'
      })
      const res = await api.get(`/matches/search?${params.toString()}`)
      setResults(res.data)
    } catch (err: any) {
      setMessage('Error searching')
    }
  }

  const geolocate = () => {
    if (!navigator.geolocation) return
    navigator.geolocation.getCurrentPosition((pos) => {
      setForm((f) => ({ ...f, latitude: String(pos.coords.latitude), longitude: String(pos.coords.longitude) }))
    })
  }

  const alertTop = async () => {
    try {
      // For demo, create a temporary patient and alert
      const patient = {
        name: 'Requester', contact_email: '', contact_phone: '',
        blood_group_needed: form.blood_group, donation_type: form.donation_type, organ: form.organ,
        latitude: Number(form.latitude), longitude: Number(form.longitude)
      }
      const p = await api.post('/patients/', patient)
      const res = await api.post(`/notifications/alert/${p.data.id}?top_n=5`)
      setMessage(`Alerts sent: ${res.data.sent}/${res.data.requested}`)
    } catch (err) {
      setMessage('Failed to send alerts')
    }
  }

  return (
    <div>
      <form onSubmit={search} style={{ display: 'grid', gap: 8, maxWidth: 520 }}>
        <label>
          Blood group needed:
          <select value={form.blood_group} onChange={e=>setForm({...form, blood_group: e.target.value})}>
            {BLOOD_GROUPS.map(bg => <option key={bg} value={bg}>{bg}</option>)}
          </select>
        </label>
        <div style={{ display: 'flex', gap: 8 }}>
          <input placeholder="Latitude" value={form.latitude} onChange={e=>setForm({...form, latitude: e.target.value})} required />
          <input placeholder="Longitude" value={form.longitude} onChange={e=>setForm({...form, longitude: e.target.value})} required />
          <button type="button" onClick={geolocate}>Use my location</button>
        </div>
        <div>
          <label><input type="radio" name="dtype" checked={form.donation_type==='blood'} onChange={()=>setForm({...form, donation_type:'blood'})} /> Blood</label>{' '}
          <label><input type="radio" name="dtype" checked={form.donation_type==='organ'} onChange={()=>setForm({...form, donation_type:'organ'})} /> Organ</label>
        </div>
        {form.donation_type==='organ' && (
          <input placeholder="Organ (e.g., kidney)" value={form.organ} onChange={e=>setForm({...form, organ: e.target.value})} />
        )}
        <button type="submit">Search</button>
      </form>

      <div style={{ marginTop: 16 }}>
        <button onClick={alertTop} disabled={results.length===0}>Alert top donors</button>
        {message && <div style={{ marginTop: 8 }}>{message}</div>}
      </div>

      <ul style={{ marginTop: 16 }}>
        {results.map((r, idx) => (
          <li key={idx}>
            <strong>{r.donor.name}</strong> — {r.donor.blood_group} — {r.distance_km} km — Reliability: {r.reliability}
          </li>
        ))}
      </ul>
    </div>
  )
}