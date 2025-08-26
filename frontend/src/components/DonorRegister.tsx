import React, { useState } from 'react'
import { api } from '../lib/api'

const BLOOD_GROUPS = ['O-', 'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+']

export default function DonorRegister() {
  const [form, setForm] = useState({
    name: '', email: '', phone: '', blood_group: 'O+',
    latitude: '', longitude: '', city: '', state: '', country: '', donation_types: ['blood'] as string[]
  })
  const [message, setMessage] = useState('')

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    setMessage('')
    try {
      const payload = { ...form, latitude: Number(form.latitude), longitude: Number(form.longitude) }
      const res = await api.post('/donors/', payload)
      setMessage(`Registered donor #${res.data.id}`)
    } catch (err: any) {
      setMessage(err?.response?.data?.detail || 'Error registering donor')
    }
  }

  const geolocate = () => {
    if (!navigator.geolocation) return
    navigator.geolocation.getCurrentPosition((pos) => {
      setForm((f) => ({ ...f, latitude: String(pos.coords.latitude), longitude: String(pos.coords.longitude) }))
    })
  }

  const toggleType = (type: string) => {
    setForm((f) => {
      const set = new Set(f.donation_types)
      if (set.has(type)) set.delete(type); else set.add(type)
      return { ...f, donation_types: Array.from(set) }
    })
  }

  return (
    <form onSubmit={submit} style={{ display: 'grid', gap: 8, maxWidth: 520 }}>
      <input placeholder="Full name" value={form.name} onChange={e=>setForm({...form, name: e.target.value})} required />
      <input placeholder="Email" value={form.email} onChange={e=>setForm({...form, email: e.target.value})} required />
      <input placeholder="Phone" value={form.phone} onChange={e=>setForm({...form, phone: e.target.value})} />

      <label>
        Blood group:
        <select value={form.blood_group} onChange={e=>setForm({...form, blood_group: e.target.value})}>
          {BLOOD_GROUPS.map(bg => <option key={bg} value={bg}>{bg}</option>)}
        </select>
      </label>

      <div style={{ display: 'flex', gap: 8 }}>
        <input placeholder="Latitude" value={form.latitude} onChange={e=>setForm({...form, latitude: e.target.value})} required />
        <input placeholder="Longitude" value={form.longitude} onChange={e=>setForm({...form, longitude: e.target.value})} required />
        <button type="button" onClick={geolocate}>Use my location</button>
      </div>

      <div style={{ display: 'flex', gap: 8 }}>
        <input placeholder="City" value={form.city} onChange={e=>setForm({...form, city: e.target.value})} />
        <input placeholder="State" value={form.state} onChange={e=>setForm({...form, state: e.target.value})} />
        <input placeholder="Country" value={form.country} onChange={e=>setForm({...form, country: e.target.value})} />
      </div>

      <div>
        <label><input type="checkbox" checked={form.donation_types.includes('blood')} onChange={()=>toggleType('blood')} /> Blood</label>{' '}
        <label><input type="checkbox" checked={form.donation_types.includes('organ')} onChange={()=>toggleType('organ')} /> Organ</label>
      </div>

      <button type="submit">Register</button>
      {message && <div>{message}</div>}
    </form>
  )
}