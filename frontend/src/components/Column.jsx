import { TicketCard } from './TicketCard'

export function Column({ name, bucket, tickets, now }) {
  return (
    <section className={`column ${bucket}`}>
      <h2>{name} <span className="count">{tickets.length}</span></h2>
      {tickets.map((ticket) => (
        <TicketCard key={ticket.id} ticket={ticket} now={now} />
      ))}
    </section>
  )
}
