export function timeLeft(dueAt, now) {
  const minutes = Math.round((new Date(dueAt) - now) / 60000)
  const abs = Math.abs(minutes)
  const hours = Math.floor(abs / 60)
  const rest = abs % 60
  const text = hours > 0 ? `${hours}h ${rest}m` : `${rest}m`
  return minutes < 0 ? `${text} over` : `${text} left`
}

export function formatDue(dueAt, timeZone) {
  return new Date(dueAt).toLocaleString('en-CA', {
    timeZone,
    weekday: 'short',
    hour: '2-digit',
    minute: '2-digit',
    timeZoneName: 'short',
  })
}
