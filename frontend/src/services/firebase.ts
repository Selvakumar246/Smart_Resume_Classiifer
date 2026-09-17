import { initializeApp, getApps, type FirebaseApp } from 'firebase/app'
import {
  getAuth,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  updateProfile,
  signInWithPopup,
  signInWithRedirect,
  getRedirectResult,
  GoogleAuthProvider,
  signOut,
  type Auth,
  type UserCredential
} from 'firebase/auth'

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
}

export const isFirebaseConfigured = Boolean(
  firebaseConfig.apiKey &&
  firebaseConfig.projectId &&
  firebaseConfig.apiKey !== ''
)

let app: FirebaseApp | undefined
let auth: Auth | undefined

if (isFirebaseConfigured) {
  app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApps()[0]
  auth = getAuth(app)
}

export { auth }

export async function registerWithFirebase(email: string, password: string, displayName: string): Promise<{ credential: UserCredential; token: string }> {
  if (!auth) throw new Error('Firebase Auth is not configured in .env variables.')
  const credential = await createUserWithEmailAndPassword(auth, email, password)
  if (displayName && credential.user) {
    await updateProfile(credential.user, { displayName })
  }
  const token = await credential.user.getIdToken()
  return { credential, token }
}

export async function loginWithFirebase(email: string, password: string): Promise<{ credential: UserCredential; token: string }> {
  if (!auth) throw new Error('Firebase Auth is not configured in .env variables.')
  const credential = await signInWithEmailAndPassword(auth, email, password)
  const token = await credential.user.getIdToken()
  return { credential, token }
}

export async function loginWithGoogleFirebase(): Promise<{ credential: UserCredential; token: string }> {
  if (!auth) throw new Error('Firebase Auth is not configured in .env variables.')
  const provider = new GoogleAuthProvider()
  provider.setCustomParameters({ prompt: 'select_account' })
  const credential = await signInWithPopup(auth, provider)
  const token = await credential.user.getIdToken()
  return { credential, token }
}

export async function logoutFirebase(): Promise<void> {
  if (auth) {
    await signOut(auth)
  }
}

export async function getCurrentFirebaseToken(): Promise<string | null> {
  if (!auth || !auth.currentUser) return null
  return auth.currentUser.getIdToken(/* forceRefresh */ true)
}
