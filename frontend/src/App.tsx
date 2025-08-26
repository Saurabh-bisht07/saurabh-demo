import React, { useState } from 'react'
import DonorRegister from './components/DonorRegister'
import PatientSearch from './components/PatientSearch'

export default function App() {
  const [tab, setTab] = useState<'register' | 'search'>('register')
  return (
    <div style={{ fontFamily: 'sans-serif', padding: 20 }}>
      <h1>Blood & Organ Donation Matcher</h1>
      <div style={{ display: 'flex', gap: 12, marginBottom: 16 }}>
        <button onClick={() => setTab('register')} disabled={tab==='register'}>Register as Donor</button>
        <button onClick={() => setTab('search')} disabled={tab==='search'}>Find Donors</button>
      </div>
      {tab === 'register' ? <DonorRegister /> : <PatientSearch />}
    </div>
  )
}