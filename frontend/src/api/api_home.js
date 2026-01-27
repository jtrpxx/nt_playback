// // Simple API wrapper for home-related calls
// import { API_AUDIO_LIST } from './paths'

// export async function getAudioList({ start = 0, length = 50, search = '' } = {}, token) {
//   const params = new URLSearchParams({
//     draw: '1',
//     start: String(start),
//     length: String(length),
//     'search[value]': search || ''
//   })

//   const headers = {}
//   if (token) headers['Authorization'] = `Bearer ${token}`

//   // If token provided, send Authorization header. If not, assume session-cookie auth and
//   // include cookies for cross-origin requests via credentials: 'include'.
//   const res = await fetch(`${API_AUDIO_LIST()}?${params.toString()}`, {
//     method: 'GET',
//     headers,
//     credentials: token ? 'omit' : 'include'
//   })

//   if (!res.ok) {
//     const txt = await res.text().catch(() => '')
//     throw new Error(`API error ${res.status}: ${txt}`)
//   }

//   return res.json()
// }
