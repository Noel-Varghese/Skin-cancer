import { useState } from 'react'
import Landing from './Landing'
import Scanner from './Scanner'

export default function App() {
  const [started, setStarted] = useState(false)
  return started
    ? <Scanner onBack={() => setStarted(false)} />
    : <Landing onStart={() => setStarted(true)} />
}
