import { Column } from './Column'

const COLUMNS = [
  { bucket: 'at_risk', name: 'At risk' },
  { bucket: 'on_time', name: 'On time' },
  { bucket: 'breached', name: 'Breached' },
  { bucket: 'paused', name: 'Paused' },
]

export function Board({ tickets, now }) {
  return (
    <div className="board">
      {COLUMNS.map((column) => (
        <Column
          key={column.bucket}
          name={column.name}
          bucket={column.bucket}
          tickets={tickets.filter((t) => t.bucket === column.bucket)}
          now={now}
        />
      ))}
    </div>
  )
}
