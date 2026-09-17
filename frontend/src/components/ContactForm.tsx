import { CheckCircle2, LoaderCircle, Send } from 'lucide-react'
import { useState, type FormEvent } from 'react'
import { api } from '../services/api'

export function ContactForm() {
  const [form, setForm] = useState({ name: '', email: '', subject: '', message: '' })
  const [loading, setLoading] = useState(false)
  const [status, setStatus] = useState('')
  const [error, setError] = useState('')
  const submit = async (event: FormEvent) => {
    event.preventDefault(); setLoading(true); setStatus(''); setError('')
    try {
      const response = await api.sendFeedback(form)
      setStatus(response.message)
      setForm({ name: '', email: '', subject: '', message: '' })
    } catch (caught) { setError(caught instanceof Error ? caught.message : 'Could not send your message.') }
    finally { setLoading(false) }
  }
  const update = (key: keyof typeof form, value: string) => setForm((current) => ({ ...current, [key]: value }))
  return <form onSubmit={submit} className="card"><div className="grid gap-4 sm:grid-cols-2"><div><label className="label" htmlFor="contact-name">Name</label><input id="contact-name" className="input" required minLength={2} value={form.name} onChange={(e) => update('name', e.target.value)} placeholder="Your name" /></div><div><label className="label" htmlFor="contact-email">Email</label><input id="contact-email" className="input" required type="email" value={form.email} onChange={(e) => update('email', e.target.value)} placeholder="you@example.com" /></div></div><div className="mt-4"><label className="label" htmlFor="contact-subject">Subject</label><input id="contact-subject" className="input" required minLength={3} value={form.subject} onChange={(e) => update('subject', e.target.value)} placeholder="How can we help?" /></div><div className="mt-4"><label className="label" htmlFor="contact-message">Message</label><textarea id="contact-message" className="input min-h-32 resize-y" required minLength={5} value={form.message} onChange={(e) => update('message', e.target.value)} placeholder="Share a question, feedback, or partnership request." /></div>{status && <div className="mt-4 flex gap-2 rounded-2xl bg-emerald-50 p-3 text-sm text-emerald-800 dark:bg-emerald-500/10 dark:text-emerald-200"><CheckCircle2 size={17} />{status}</div>}{error && <div className="mt-4 rounded-2xl bg-rose-50 p-3 text-sm text-rose-700 dark:bg-rose-500/10 dark:text-rose-300">{error}</div>}<button disabled={loading} className="button-primary mt-5 w-full sm:w-auto">{loading ? <LoaderCircle size={17} className="animate-spin" /> : <Send size={17} />} Send message</button></form>
}
