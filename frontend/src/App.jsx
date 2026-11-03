import { useState } from 'react'
import Field from './Field'
import Landing from './Landing'
import Scanner from './Scanner'

export default function App() {
  const [view, setView] = useState('home')
  const [leaving, setLeaving] = useState(false)

  // Fade-zoom out, swap screens, fade-zoom in
  const go = (next) => {
    if (leaving) return
    setLeaving(true)
    setTimeout(() => { setView(next); setLeaving(false) }, 450)
  }

  return (
    <>
      <Field />
      <div className={leaving ? 'leave' : 'enter'}>
        {view === 'home'
          ? <Landing onStart={() => go('scan')} />
          : <Scanner onBack={() => go('home')} />}
      </div>
    </>
  )
}
