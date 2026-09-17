import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from 'react'
import { api } from '../services/api'
import type { User } from '../types'

import { logoutFirebase } from '../services/firebase'

type AuthContextValue = {
  user: User | null
  loading: boolean
  setSession: (token: string, user?: User) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const stored = localStorage.getItem('resume_ai_token')
    if (!stored) { setLoading(false); return }
    api.me().then(setUser).catch(() => localStorage.removeItem('resume_ai_token')).finally(() => setLoading(false))
  }, [])

  const value = useMemo<AuthContextValue>(() => ({
    user,
    loading,
    setSession: async (token, nextUser) => {
      localStorage.setItem('resume_ai_token', token)
      setUser(nextUser || await api.me())
    },
    logout: () => {
      localStorage.removeItem('resume_ai_token')
      logoutFirebase().catch(() => {})
      setUser(null)
    },
  }), [loading, user])

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth must be used inside AuthProvider')
  return context
}
