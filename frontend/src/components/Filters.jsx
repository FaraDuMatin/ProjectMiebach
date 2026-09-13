const PRIORITIES = ['P1', 'P2', 'P3', 'P4']

export function Filters({ countries, country, priority, onChange }) {
  return (
    <div className="filters">
      <select value={country} onChange={(e) => onChange({ country: e.target.value, priority })}>
        <option value="">All countries</option>
        {countries.map((c) => (
          <option key={c.code} value={c.code}>{c.name}</option>
        ))}
      </select>
      <select value={priority} onChange={(e) => onChange({ country, priority: e.target.value })}>
        <option value="">All priorities</option>
        {PRIORITIES.map((p) => (
          <option key={p} value={p}>{p}</option>
        ))}
      </select>
    </div>
  )
}
