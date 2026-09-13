function getCookie(name) {
  const parts = document.cookie.split('; ')
  for (const part of parts) {
    const [key, value] = part.split('=')
    if (key === name) return value
  }
  return ''
}

export async function apiGet(path) {
  const response = await fetch(path)
  if (!response.ok) throw new Error(`${response.status} on ${path}`)
  return response.json()
}

export async function apiPost(path, body) {
  const response = await fetch(path, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify(body),
  })
  if (!response.ok) throw new Error(`${response.status} on ${path}`)
  if (response.status === 204) return null
  return response.json()
}
