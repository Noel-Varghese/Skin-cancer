import { useEffect, useRef, useState } from 'react'

const API = 'http://127.0.0.1:8000/predict'
const OK_TYPE = /^(image\/|video\/(mp4|quicktime|x-msvideo))/
const sleep = (ms) => new Promise((r) => setTimeout(r, ms))

function Brackets() {
  const c = 'absolute h-6 w-6 border-beam'
  return (
    <>
      <i className={`${c} left-3 top-3 border-l-2 border-t-2`} />
      <i className={`${c} right-3 top-3 border-r-2 border-t-2`} />
      <i className={`${c} bottom-3 left-3 border-b-2 border-l-2`} />
      <i className={`${c} bottom-3 right-3 border-b-2 border-r-2`} />
    </>
  )
}

function Ring({ value, danger }) {
  const [on, setOn] = useState(false)
  useEffect(() => { const t = setTimeout(() => setOn(true), 60); return () => clearTimeout(t) }, [])
  const C = 2 * Math.PI * 54
  const pct = Math.max(0, Math.min(100, Number(value) || 0))
  return (
    <div className="relative h-36 w-36 shrink-0">
      <svg viewBox="0 0 120 120" className="-rotate-90" role="img" aria-label={`Confidence ${pct.toFixed(0)} percent`}>
        <circle cx="60" cy="60" r="54" fill="none" stroke="rgba(255,255,255,.08)" strokeWidth="8" />
        <circle
          cx="60" cy="60" r="54" fill="none" strokeWidth="8" strokeLinecap="round"
          stroke={danger ? '#ff7070' : '#6ee7b7'} strokeDasharray={C}
          strokeDashoffset={on ? C * (1 - pct / 100) : C}
          style={{ transition: 'stroke-dashoffset 1.4s cubic-bezier(.2,.7,.2,1)' }}
        />
      </svg>
      <div className="absolute inset-0 grid place-items-center text-center">
        <div>
          <div className="font-display text-4xl">{pct.toFixed(1)}<span className="text-lg">%</span></div>
          <div className="text-xs text-slate-400">confidence</div>
        </div>
      </div>
    </div>
  )
}

function Verdict({ result }) {
  const danger = result.diagnosis.includes('DANGER')
  const label = result.diagnosis.replace(' (DANGER)', '')
  const precancer = label.includes('Actinic')
  const advice = danger
    ? 'This pattern resembles a cancerous lesion type. Please see a dermatologist soon.'
    : precancer
      ? 'Actinic keratoses can be precancerous. Worth showing to a doctor.'
      : 'This pattern resembles a usually harmless type. Keep an eye on it and get any change checked.'

  return (
    <div className="fade">
      <p className="text-sm text-slate-400">Closest match</p>
      <h2 className={`font-display mt-1 text-4xl leading-tight ${danger ? 'text-alert' : 'text-safe'}`}>{label}</h2>
      <div className="mt-6 flex items-center gap-6">
        <Ring value={result.confidence} danger={danger} />
        <p className="text-sm leading-relaxed text-slate-300">
          {advice}
          {result.confidence < 60 && (
            <span className="mt-2 block text-slate-400">The model is unsure here, so treat this result with extra caution.</span>
          )}
        </p>
      </div>
    </div>
  )
}

export default function Scanner({ onBack }) {
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)
  const [drag, setDrag] = useState(false)
  const input = useRef(null)

  useEffect(() => () => { if (preview) URL.revokeObjectURL(preview) }, [preview])

  const pick = (f) => {
    if (!f) return
    if (!OK_TYPE.test(f.type)) return setError('Use an image, or an MP4, MOV or AVI video.')
    setFile(f); setPreview(URL.createObjectURL(f)); setResult(null); setError(null)
  }

  const reset = () => { setFile(null); setPreview(null); setResult(null); setError(null) }

  const analyze = async () => {
    setLoading(true); setError(null); setResult(null)
    try {
      const body = new FormData()
      body.append('file', file)
      const [res] = await Promise.all([fetch(API, { method: 'POST', body }), sleep(1600)])
      if (!res.ok) throw new Error('bad response')
      setResult(await res.json())
    } catch {
      setError('Could not reach the AI engine. Start the backend (api.py on port 8000) and try again.')
    }
    setLoading(false)
  }

  const isVideo = file?.type.startsWith('video/')

  return (
    <main className="fade mx-auto min-h-screen max-w-5xl px-6 py-6 md:px-10">
      <header className="flex items-center justify-between">
        <button onClick={onBack} className="font-display text-2xl tracking-wide">DermAI</button>
        {file && <button onClick={reset} className="text-sm text-slate-400 hover:text-white">Start over</button>}
      </header>

      <div className="mt-8 grid gap-6 md:grid-cols-2">
        {/* Left: upload / preview */}
        <section className="glass p-5">
          {!preview ? (
            <label
              onDragOver={(e) => { e.preventDefault(); setDrag(true) }}
              onDragLeave={() => setDrag(false)}
              onDrop={(e) => { e.preventDefault(); setDrag(false); pick(e.dataTransfer.files[0]) }}
              className={`grid min-h-[360px] cursor-pointer place-items-center rounded-2xl border-2 border-dashed p-6 text-center transition ${drag ? 'border-beam bg-beam/10' : 'border-white/15 hover:border-beam/60'}`}
            >
              <div>
                <div className="mx-auto mb-4 grid h-14 w-14 place-items-center rounded-full bg-skin/15 text-2xl text-skin">+</div>
                <p className="font-display text-2xl">Drop a photo or video here</p>
                <p className="mt-2 text-sm text-slate-400">or click to browse. JPG, PNG, GIF, MP4, MOV, AVI</p>
              </div>
              <input ref={input} type="file" className="sr-only" accept="image/*,video/mp4,video/quicktime,video/x-msvideo,.gif" onChange={(e) => pick(e.target.files[0])} />
            </label>
          ) : (
            <div className="relative overflow-hidden rounded-2xl bg-black/40">
              {isVideo
                ? <video src={preview} className="h-[360px] w-full object-contain" muted loop autoPlay playsInline />
                : <img src={preview} alt="Selected skin spot" className="h-[360px] w-full object-contain" />}
              <Brackets />
              {loading && <span className="beam" />}
            </div>
          )}

          {error && <p role="alert" className="mt-4 rounded-xl border border-alert/40 bg-alert/10 p-3 text-sm text-alert">{error}</p>}

          <button className="cta mt-5 w-full" disabled={!file || loading} onClick={analyze}>
            {loading ? 'Scanning...' : result ? 'Scan again' : 'Analyse this spot'}
          </button>
        </section>

        {/* Right: status / result */}
        <section className="glass flex min-h-[420px] flex-col justify-center p-7">
          {result ? <Verdict result={result} />
            : loading ? (
              <div className="fade text-center">
                <div className="mx-auto mb-5 h-14 w-14 animate-spin rounded-full border-2 border-white/10 border-t-beam" />
                <p className="font-display text-2xl">Reading the pattern</p>
                <p className="mt-2 text-sm text-slate-400">Checking shape, border and colour</p>
              </div>
            ) : (
              <div>
                <h2 className="font-display text-3xl">For a clear result</h2>
                <ul className="mt-5 space-y-4 text-slate-300">
                  <li>Use good, even light with no flash glare.</li>
                  <li>Get close, so the spot fills most of the frame.</li>
                  <li>Keep it sharp. Hold still or rest your hand on the skin.</li>
                </ul>
              </div>
            )}
        </section>
      </div>

      <p className="mt-8 text-center text-xs text-slate-500">
        Research prototype, not a medical device. Only a doctor can diagnose skin cancer.
      </p>
    </main>
  )
}
