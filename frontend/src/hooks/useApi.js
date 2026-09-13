import { useEffect, useState } from 'react'
import { apiGet } from '../api'

export function useApi(path, refreshMs) {
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    let active = true

    function load() {
      apiGet(path)
        .then((result) => {
          if (active) setData(result)
        })
        .catch((err) => {
          if (active) setError(err.message)
        })
    }

    load()
    const timer = refreshMs ? setInterval(load, refreshMs) : null
    return () => {
      active = false
      if (timer) clearInterval(timer)
    }
  }, [path, refreshMs])

  return { data, error }
}
