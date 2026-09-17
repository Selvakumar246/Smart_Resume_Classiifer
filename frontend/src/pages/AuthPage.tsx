import { ArrowLeft, Check, Eye, EyeOff, LoaderCircle, ShieldCheck } from 'lucide-react'
import { useState, type FormEvent } from 'react'
import { Link, Navigate, useNavigate } from 'react-router-dom'
import { Logo } from '../components/Logo'
import { ThemeToggle } from '../components/ThemeToggle'
import { useAuth } from '../context/AuthContext'
import { api } from '../services/api'
import { isFirebaseConfigured, loginWithFirebase, loginWithGoogleFirebase, registerWithFirebase } from '../services/firebase'

export function AuthPage({ mode }: { mode: 'login' | 'register' }) {
  const { user, setSession } = useAuth()
  const navigate = useNavigate()
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [show, setShow] = useState(false)
  const [remember, setRemember] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  if (user) return <Navigate to="/app" replace />

  const formatFirebaseError = (err: any): string => {
    const message = err?.message || err?.code || String(err)
    if (message.includes('Failed to fetch') || message.includes('fetch failed') || message.includes('NetworkError') || message.includes('NETWORK_ERROR')) {
      return 'Backend server is not running or unreachable at http://localhost:8000. Please run run-windows-fixed.bat.'
    }
    if (message.includes('auth/invalid-credential') || message.includes('auth/wrong-password')) return 'Incorrect email or password.'
    if (message.includes('auth/user-not-found')) return 'No account found with this email. Please register first.'
    if (message.includes('auth/email-already-in-use')) return 'An account with this email already exists. Please sign in instead.'
    if (message.includes('auth/weak-password')) return 'Password should be at least 6 characters long.'
    if (message.includes('auth/too-many-requests')) return 'Too many failed attempts. Please wait a moment and try again.'
    if (message.includes('auth/network-request-failed')) return 'Network error. Please check your internet connection.'
    if (message.includes('auth/popup-closed-by-user')) return ''  // Not an error
    return message
  }

  const submit = async (event: FormEvent) => {
    event.preventDefault(); setError(''); setLoading(true)
    const cleanEmail = email.trim().toLowerCase()
    try {
      if (isFirebaseConfigured) {
        try {
          let token: string
          if (mode === 'login') {
            // Try Firebase login first
            try {
              const res = await loginWithFirebase(cleanEmail, password)
              token = res.token
            } catch (fbLoginErr: any) {
              const fbMsg = fbLoginErr?.message || fbLoginErr?.code || ''
              // If user not found in Firebase, try backend direct login
              if (fbMsg.includes('auth/user-not-found') || fbMsg.includes('auth/invalid-credential')) {
                try {
                  const response = await api.login(cleanEmail, password, remember)
                  await setSession(response.access_token, response.user)
                  navigate('/app')
                  return
                } catch (backendErr: any) {
                  throw backendErr
                }
              }
              throw fbLoginErr
            }
            const response = await api.firebaseAuth(token)
            await setSession(response.access_token, response.user)
            navigate('/app')
            return
          } else {
            // Register mode
            try {
              const res = await registerWithFirebase(cleanEmail, password, name.trim())
              token = res.token
            } catch (fbRegErr: any) {
              const fbMsg = fbRegErr?.message || fbRegErr?.code || ''
              // If email already exists in Firebase, try to login instead
              if (fbMsg.includes('auth/email-already-in-use')) {
                try {
                  const res = await loginWithFirebase(cleanEmail, password)
                  token = res.token
                } catch {
                  throw new Error('An account with this email already exists. Please sign in instead.')
                }
              } else {
                throw fbRegErr
              }
            }
            const response = await api.firebaseAuth(token)
            await setSession(response.access_token, response.user)
            navigate('/app')
            return
          }
        } catch (fbErr: any) {
          const fbMsg = fbErr?.message || fbErr?.code || ''
          // If Firebase itself is broken (bad API key), fall back to backend-only auth
          if (fbMsg.includes('auth/api-key-not-valid') || fbMsg.includes('invalid-api-key') || fbMsg.includes('auth/configuration-not-found')) {
            const response = mode === 'login'
              ? await api.login(cleanEmail, password, remember)
              : await api.register(name.trim(), cleanEmail, password)
            await setSession(response.access_token, response.user)
            navigate('/app')
            return
          }
          throw fbErr
        }
      } else {
        // No Firebase configured — use backend directly
        const response = mode === 'login' 
          ? await api.login(cleanEmail, password, remember) 
          : await api.register(name.trim(), cleanEmail, password)
        await setSession(response.access_token, response.user)
        navigate('/app')
      }
    } catch (caught: any) { 
      const msg = formatFirebaseError(caught)
      if (msg) setError(msg)
    } finally { 
      setLoading(false) 
    }
  }

  const handleGoogleLogin = async () => {
    if (isFirebaseConfigured) {
      setError(''); setLoading(true)
      try {
        const res = await loginWithGoogleFirebase()
        const response = await api.firebaseAuth(res.token)
        await setSession(response.access_token, response.user)
        navigate('/app')
      } catch (caught: any) {
        if (caught?.code === 'auth/popup-closed-by-user') return
        setError(formatFirebaseError(caught))
      } finally {
        setLoading(false)
      }
    } else {
      window.location.href = api.googleLoginUrl
    }
  }

  return (
    <div className="app-shell min-h-screen">
      <div className="grid min-h-screen lg:grid-cols-[1.05fr_.95fr]">
        <aside className="relative hidden overflow-hidden bg-slate-900 p-12 text-white lg:flex lg:flex-col">
          <div className="relative">
            <Logo />
            <div className="mt-20 max-w-lg">
              <span className="eyebrow border-slate-700 bg-slate-800 text-teal-300">Resume intelligence platform</span>
              <h1 className="mt-6 font-display text-4xl font-extrabold leading-tight tracking-tight sm:text-5xl">
                Turn every resume into a structured career plan.
              </h1>
              <p className="mt-4 text-base leading-7 text-slate-300">
                Evaluate career fit, ATS format quality, job description alignment, skill gaps, and interview prep in one clean workflow.
              </p>
            </div>
            <div className="mt-10 space-y-3.5">
              {[
                'Multi-category taxonomy career predictions',
                'Transparent ATS deductions & format analysis',
                'Private history & downloadable PDF reports'
              ].map((item) => (
                <div key={item} className="flex items-center gap-3 text-sm font-semibold text-slate-200">
                  <span className="grid h-6 w-6 place-items-center rounded-full bg-teal-500/20 text-teal-300">
                    <Check size={14} />
                  </span>
                  {item}
                </div>
              ))}
            </div>
          </div>
          <div className="relative mt-auto flex items-center gap-3 rounded-xl border border-slate-800 bg-slate-800/50 p-4">
            <ShieldCheck className="text-teal-400" />
            <p className="text-xs leading-5 text-slate-300">Encrypted JWT session authentication enabled.</p>
          </div>
        </aside>

        <main className="flex min-h-screen flex-col p-4 sm:p-7">
          <div className="flex items-center justify-between">
            <Link to="/" className="inline-flex items-center gap-2 text-sm font-semibold text-slate-600 hover:text-teal-700 dark:text-slate-400 dark:hover:text-teal-400">
              <ArrowLeft size={17} /> Back home
            </Link>
            <ThemeToggle />
          </div>

          <div className="mx-auto flex w-full max-w-md flex-1 flex-col justify-center py-10">
            <div className="lg:hidden"><Logo /></div>
            <div className="mt-8 lg:mt-0">
              <p className="text-xs font-bold uppercase tracking-[.14em] text-teal-700 dark:text-teal-400">
                {mode === 'login' ? 'Welcome back' : 'Create your account'}
              </p>
              <h2 className="mt-1.5 font-display text-3xl font-extrabold tracking-tight">
                {mode === 'login' ? 'Sign in to your account' : 'Get started in seconds'}
              </h2>
              <p className="mt-2 text-sm leading-6 text-slate-500">
                {mode === 'login' ? 'Access your reports, history, and workspace.' : 'Free plan includes three resume analyses every month.'}
              </p>
            </div>

            <form onSubmit={submit} className="mt-8 space-y-4">
              {mode === 'register' && (
                <div>
                  <label className="label" htmlFor="name">Full name</label>
                  <input id="name" className="input" value={name} onChange={(e) => setName(e.target.value)} placeholder="Your full name" required minLength={2} autoComplete="name" />
                </div>
              )}
              <div>
                <label className="label" htmlFor="email">Email address</label>
                <input id="email" className="input" type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" required autoComplete="email" />
              </div>
              <div>
                <div className="mb-1.5 flex justify-between">
                  <label className="label mb-0" htmlFor="password">Password</label>
                  {mode === 'login' && <Link to="/forgot-password" className="text-xs font-semibold text-teal-700 hover:underline dark:text-teal-400">Forgot password?</Link>}
                </div>
                <div className="relative">
                  <input id="password" className="input pr-11" type={show ? 'text' : 'password'} value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Minimum 6 characters" required minLength={6} autoComplete={mode === 'login' ? 'current-password' : 'new-password'} />
                  <button type="button" onClick={() => setShow(!show)} className="absolute right-2.5 top-1/2 -translate-y-1/2 p-1.5 text-slate-400 hover:text-slate-600" aria-label={show ? 'Hide password' : 'Show password'}>
                    {show ? <EyeOff size={18} /> : <Eye size={18} />}
                  </button>
                </div>
              </div>

              {mode === 'login' && (
                <label className="flex cursor-pointer items-center gap-2.5 text-xs font-semibold text-slate-600 dark:text-slate-300">
                  <input type="checkbox" checked={remember} onChange={(e) => setRemember(e.target.checked)} className="h-4 w-4 rounded border-slate-300 text-teal-600 focus:ring-teal-500" />
                  Remember me for 30 days
                </label>
              )}

              {error && (
                <div role="alert" className="rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-xs font-semibold text-rose-700 dark:border-rose-500/20 dark:bg-rose-500/10 dark:text-rose-300">
                  {error}
                </div>
              )}

              <button disabled={loading} className="button-primary w-full">
                {loading && <LoaderCircle size={17} className="animate-spin" />}
                {mode === 'login' ? 'Sign in' : 'Create account'}
              </button>
            </form>

            <div className="my-6 flex items-center gap-3 text-xs text-slate-400">
              <span className="h-px flex-1 bg-slate-200 dark:bg-slate-800" />or<span className="h-px flex-1 bg-slate-200 dark:bg-slate-800" />
            </div>

            <button type="button" onClick={handleGoogleLogin} className="button-secondary w-full">
              <svg viewBox="0 0 24 24" className="h-4 w-4"><path fill="#4285F4" d="M21.6 12.23c0-.71-.06-1.4-.18-2.07H12v3.91h5.38a4.6 4.6 0 0 1-2 3.02v2.54h3.24c1.9-1.75 2.98-4.33 2.98-7.4Z"/><path fill="#34A853" d="M12 22c2.7 0 4.97-.9 6.62-2.42l-3.24-2.54c-.9.6-2.05.96-3.38.96-2.61 0-4.82-1.76-5.61-4.13H3.04v2.62A10 10 0 0 0 12 22Z"/><path fill="#FBBC05" d="M6.39 13.87A6 6 0 0 1 6.08 12c0-.65.11-1.28.31-1.87V7.51H3.04A10 10 0 0 0 2 12c0 1.61.38 3.14 1.04 4.49l3.35-2.62Z"/><path fill="#EA4335" d="M12 6c1.47 0 2.79.51 3.83 1.5l2.87-2.87A9.62 9.62 0 0 0 12 2a10 10 0 0 0-8.96 5.51l3.35 2.62C7.18 7.76 9.39 6 12 6Z"/></svg>
              Continue with Google
            </button>

            <p className="mt-6 text-center text-xs text-slate-500">
              {mode === 'login' ? "Don't have an account?" : 'Already have an account?'} {' '}
              <Link to={mode === 'login' ? '/register' : '/login'} className="font-bold text-teal-700 hover:underline dark:text-teal-400">
                {mode === 'login' ? 'Create one' : 'Sign in'}
              </Link>
            </p>
          </div>
        </main>
      </div>
    </div>
  )
}
