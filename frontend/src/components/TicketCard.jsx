import { formatDue, timeLeft } from '../time'

export function TicketCard({ ticket, now }) {
  return (
    <article className={`card ${ticket.bucket}`}>
      <header>
        <a href={ticket.jira_url} target="_blank" rel="noreferrer">{ticket.jira_key}</a>
        <span className="priority">{ticket.priority}</span>
        <span className="country">{ticket.country}</span>
      </header>
      <p className="title">{ticket.title}</p>
      <footer>
        <strong>{timeLeft(ticket.due_at, now)}</strong>
        <span>{formatDue(ticket.due_at, ticket.timezone)}</span>
      </footer>
    </article>
  )
}
