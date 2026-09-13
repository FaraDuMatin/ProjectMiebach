import { useState } from 'react'
import { apiPost } from '../api'

export function Login({ onLogin }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  async function submit(event) {
    event.preventDefault()
    try {
      const user = await apiPost('/api/auth/login/', { username, password })
      onLogin(user.username)
    } catch {
      setError('Wrong username or password')
    }
  }

  return (
    <form className="login" onSubmit={submit}>
      <h1>SLA Tower</h1>
      <input placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
      <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <button type="submit">Log in</button>
      {error && <p className="error">{error}</p>}
    </form>
  )
}
