import axios from 'axios'

const baseURL = (import.meta as any).env?.VITE_API_BASE_URL || 'http://localhost:8000'

export const api = axios.create({ baseURL: `${baseURL}/api` })