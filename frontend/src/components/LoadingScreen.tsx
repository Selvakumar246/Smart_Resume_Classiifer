import { LoaderCircle } from 'lucide-react'

export function LoadingScreen({ message = 'Preparing your workspace' }: { message?: string }) {
  return <div className="grid min-h-[60vh] place-items-center"><div className="text-center"><LoaderCircle className="mx-auto mb-4 animate-spin text-blue-600" size={34} /><p className="text-sm font-medium text-slate-500">{message}</p></div></div>
}
