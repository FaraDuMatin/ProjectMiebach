import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'

export function LoadChart({ byCountry }) {
  const data = Object.keys(byCountry).map((code) => ({ country: code, tickets: byCountry[code] }))

  return (
    <div className="chart">
      <h2>Open tickets per country</h2>
      <ResponsiveContainer width="100%" height={180}>
        <BarChart data={data}>
          <XAxis dataKey="country" />
          <YAxis allowDecimals={false} width={30} />
          <Tooltip />
          <Bar dataKey="tickets" fill="var(--accent)" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
