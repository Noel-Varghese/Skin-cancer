import { useEffect, useRef } from 'react'

// Drifting particles that link up near the cursor, like a network "thinking"
function Field() {
  const ref = useRef(null)
  useEffect(() => {
    const c = ref.current
    const ctx = c.getContext('2d')
    const calm = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    const mouse = { x: -999, y: -999 }
    let w, h, raf, pts = []

    const resize = () => {
      w = c.width = window.innerWidth
      h = c.height = window.innerHeight
      const n = Math.min(80, Math.floor((w * h) / 20000))
      pts = Array.from({ length: n }, () => ({
        x: Math.random() * w, y: Math.random() * h,
        vx: (Math.random() - 0.5) * 0.35, vy: (Math.random() - 0.5) * 0.35,
      }))
    }
    const move = (e) => { mouse.x = e.clientX; mouse.y = e.clientY }

    const tick = () => {
      ctx.clearRect(0, 0, w, h)
      for (const p of pts) {
        p.x += p.vx; p.y += p.vy
        if (p.x < 0 || p.x > w) p.vx *= -1
        if (p.y < 0 || p.y > h) p.vy *= -1
        ctx.fillStyle = 'rgba(127,224,208,.55)'
        ctx.beginPath(); ctx.arc(p.x, p.y, 1.5, 0, 6.283); ctx.fill()
      }
      const all = [...pts, mouse]
      for (let i = 0; i < all.length; i++) {
        for (let j = i + 1; j < all.length; j++) {
          const d = Math.hypot(all[i].x - all[j].x, all[i].y - all[j].y)
          const max = j === all.length - 1 ? 180 : 120
          if (d < max) {
            ctx.strokeStyle = `rgba(127,224,208,${(1 - d / max) * 0.28})`
            ctx.beginPath(); ctx.moveTo(all[i].x, all[i].y); ctx.lineTo(all[j].x, all[j].y); ctx.stroke()
          }
        }
      }
      if (!calm) raf = requestAnimationFrame(tick)
    }

    resize(); tick()
    window.addEventListener('resize', resize)
    window.addEventListener('mousemove', move)
    return () => {
      cancelAnimationFrame(raf)
      window.removeEventListener('resize', resize)
      window.removeEventListener('mousemove', move)
    }
  }, [])
  return <canvas ref={ref} className="pointer-events-none fixed inset-0 opacity-70" aria-hidden="true" />
}

// The hero: a dermoscope view of a mole being scanned, annotated with the ABCDE rule
function Lens() {
  return (
    <div className="lens rise" style={{ '--d': '.35s' }} aria-hidden="true">
      <div className="ring b" /><div className="ring" /><div className="ring c" />
      <div className="skin"><span className="mole" /><span className="beam" /></div>
      <span className="tag" style={{ top: '8%', left: '-4%', '--d': '0s' }}>Asymmetry</span>
      <span className="tag r" style={{ top: '22%', right: '-6%', '--d': '.8s' }}>Border</span>
      <span className="tag" style={{ bottom: '18%', left: '-8%', '--d': '1.6s' }}>Colour</span>
      <span className="tag r" style={{ bottom: '6%', right: '-2%', '--d': '2.4s' }}>Diameter</span>
    </div>
  )
}

export default function Landing({ onStart }) {
  return (
    <main className="relative min-h-screen overflow-hidden">
      <Field />

      <header className="relative z-10 mx-auto flex max-w-6xl items-center justify-between px-6 py-6 md:px-12">
        <span className="font-display text-2xl tracking-wide">DermAI</span>
        <span className="rounded-full border border-white/10 px-3 py-1 text-xs text-slate-300">
          Runs on your machine. Nothing leaves it.
        </span>
      </header>

      <section className="relative z-10 mx-auto grid max-w-6xl items-center gap-14 px-6 pb-20 pt-6 md:px-12 lg:grid-cols-[1.1fr_1fr] lg:pt-14">
        <div>
          <h1 className="rise font-display text-6xl leading-[.95] md:text-8xl" style={{ '--d': '.1s' }}>
            Look closer at that mole.
          </h1>
          <p className="rise mt-6 max-w-md text-lg leading-relaxed text-slate-300" style={{ '--d': '.25s' }}>
            Upload a photo or short video of a skin spot. A neural network trained on 10,015 dermoscopy
            images sorts it into one of 7 lesion types in seconds.
          </p>
          <div className="rise mt-9 flex flex-wrap items-center gap-5" style={{ '--d': '.4s' }}>
            <button className="cta text-base" onClick={onStart}>Scan a spot</button>
            <span className="text-sm text-slate-400">Takes about 5 seconds</span>
          </div>
          <p className="rise mt-12 max-w-md text-xs leading-relaxed text-slate-500" style={{ '--d': '.55s' }}>
            Research prototype. It can't replace a dermatologist. If a spot changes, bleeds or worries you, book a check-up.
          </p>
        </div>
        <Lens />
      </section>
    </main>
  )
}
