import { useEffect, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { LoadingScreen } from '../components/LoadingScreen'
import { useAuth } from '../context/AuthContext'

export function AuthCallbackPage() {
  const [params] = useSearchParams()
  const navigate = useNavigate()
  const { setSession } = useAuth()
  const [error, setError] = useState('')
  useEffect(() => {
    const token = params.get('token')
    if (!token) { setError('Google authentication did not return a token.'); return }
    setSession(token).then(() => navigate('/app', { replace: true })).catch((caught) => setError(caught instanceof Error ? caught.message : 'Could not sign in.'))
  }, [navigate, params, setSession])
  return <div className="app-shell grid min-h-screen place-items-center">{error ? <div className="card max-w-md text-center"><h1 className="font-display text-xl font-bold">Sign-in failed</h1><p className="mt-3 text-sm text-rose-600">{error}</p></div> : <LoadingScreen message="Completing secure sign-in" />}</div>
}
