import { useEffect, useState } from 'react'
import { apiGet, apiPost } from './api'
import { Board } from './components/Board'
import { Filters } from './components/Filters'
import { Login } from './components/Login'
import { useApi } from './hooks/useApi'
import { useNow } from './hooks/useNow'

const REFRESH_MS = 30000

function App() {
  const [user, setUser] = useState(undefined)
  const [filters, setFilters] = useState({ country: '', priority: '' })

  useEffect(() => {
    apiGet('/api/auth/me/').then((me) => setUser(me.username))
  }, [])

  if (user === undefined) return null
  if (user === null) return <Login onLogin={setUser} />

  async function logout() {
    await apiPost('/api/auth/logout/', {})
    setUser(null)
  }

  return <Dashboard user={user} filters={filters} onFilters={setFilters} onLogout={logout} />
}

function Dashboard({ user, filters, onFilters, onLogout }) {
  const query = `?country=${filters.country}&priority=${filters.priority}`
  const tickets = useApi(`/api/tickets/${query}`, REFRESH_MS)
  const countries = useApi('/api/countries/')
  const now = useNow(60000)

  return (
    <div className="app">
      <header className="topbar">
        <h1>SLA Tower</h1>
        <Filters countries={countries.data || []} country={filters.country} priority={filters.priority} onChange={onFilters} />
        <span className="user">{user}</span>
        <button onClick={onLogout}>Log out</button>
      </header>
      {tickets.error && <p className="error">{tickets.error}</p>}
      <Board tickets={tickets.data || []} now={now} />
    </div>
  )
}

export default App
