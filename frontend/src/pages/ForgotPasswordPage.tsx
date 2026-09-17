import { ArrowLeft, CheckCircle2, KeyRound, LoaderCircle } from 'lucide-react'
import { useState, type FormEvent } from 'react'
import { Link } from 'react-router-dom'
import { Logo } from '../components/Logo'
import { ThemeToggle } from '../components/ThemeToggle'
import { api } from '../services/api'

export function ForgotPasswordPage() {
  const [email, setEmail] = useState('')
  const [token, setToken] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [complete, setComplete] = useState(false)

  const requestReset = async (event: FormEvent) => {
    event.preventDefault(); setLoading(true); setError('')
    try {
      const response = await api.forgotPassword(email)
      setMessage(response.message)
      if (response.reset_token) setToken(response.reset_token)
    } catch (caught) { setError(caught instanceof Error ? caught.message : 'Unable to request reset.') }
    finally { setLoading(false) }
  }

  const reset = async (event: FormEvent) => {
    event.preventDefault(); setLoading(true); setError('')
    try { const response = await api.resetPassword(token, password); setMessage(response.message); setComplete(true) }
    catch (caught) { setError(caught instanceof Error ? caught.message : 'Unable to reset password.') }
    finally { setLoading(false) }
  }

  return <div className="app-shell mesh-bg min-h-screen p-4 sm:p-7"><div className="flex items-center justify-between"><Logo /><ThemeToggle /></div><main className="mx-auto grid min-h-[80vh] max-w-md place-items-center"><div className="card w-full"><span className="grid h-12 w-12 place-items-center rounded-2xl bg-blue-50 text-blue-600 dark:bg-blue-500/10"><KeyRound size={21} /></span><h1 className="mt-5 font-display text-2xl font-extrabold">Reset your password</h1>{complete ? <div className="mt-6"><div className="flex gap-3 rounded-2xl bg-emerald-50 p-4 text-sm text-emerald-800 dark:bg-emerald-500/10 dark:text-emerald-200"><CheckCircle2 size={18} className="shrink-0" />{message}</div><Link to="/login" className="button-primary mt-5 w-full">Return to sign in</Link></div> : token ? <form onSubmit={reset} className="mt-6 space-y-5"><p className="text-sm leading-6 text-slate-500">Development reset token received. Set a new password below. In production, this step is opened from the email link.</p><div><label className="label" htmlFor="new-password">New password</label><input id="new-password" className="input" type="password" minLength={8} required value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Minimum 8 characters" /></div>{error && <div className="rounded-2xl bg-rose-50 p-4 text-sm text-rose-700 dark:bg-rose-500/10 dark:text-rose-300">{error}</div>}<button disabled={loading} className="button-primary w-full">{loading && <LoaderCircle size={17} className="animate-spin" />} Update password</button></form> : <form onSubmit={requestReset} className="mt-6 space-y-5"><p className="text-sm leading-6 text-slate-500">Enter your account email. Local development returns a secure reset token; production requires an email provider integration.</p><div><label className="label" htmlFor="reset-email">Email address</label><input id="reset-email" className="input" type="email" required value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" /></div>{message && <div className="rounded-2xl bg-blue-50 p-4 text-sm text-blue-800 dark:bg-blue-500/10 dark:text-blue-200">{message}</div>}{error && <div className="rounded-2xl bg-rose-50 p-4 text-sm text-rose-700 dark:bg-rose-500/10 dark:text-rose-300">{error}</div>}<button disabled={loading} className="button-primary w-full">{loading && <LoaderCircle size={17} className="animate-spin" />} Send reset instructions</button></form>}<Link to="/login" className="mt-6 inline-flex items-center gap-2 text-sm font-semibold text-slate-500 hover:text-blue-600"><ArrowLeft size={16} /> Back to sign in</Link></div></main></div>
}
