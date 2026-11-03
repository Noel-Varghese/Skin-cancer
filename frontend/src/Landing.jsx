import { useEffect, useRef, useState } from 'react'

const TAGS = [
  ['Asymmetry', { top: '8%', left: '-4%' }, ''],
  ['Border', { top: '22%', right: '-6%' }, 'r'],
  ['Colour', { bottom: '18%', left: '-8%' }, ''],
  ['Diameter', { bottom: '6%', right: '-2%' }, 'r'],
]
const ABCDE = {
  Asymmetry: 'Imagine a line through the mole. If the two halves don’t match, that’s a warning sign.',
  Border: 'Healthy moles have smooth edges. Ragged, notched or blurry borders are a warning sign.',
  Colour: 'One even shade is normal. Several browns, black, red or white patches are a warning sign.',
  Diameter: 'Wider than about 6 mm, a pencil eraser, deserves a closer look.',
}

// The hero: tilts in 3D toward your cursor. Hover a label to speed up the scan and learn the rule.
function Lens() {
  const tilt = useRef(null)
  const [tag, setTag] = useState(null)

  useEffect(() => {
    const onMove = (e) => {
      const x = e.clientX / window.innerWidth - 0.5, y = e.clientY / window.innerHeight - 0.5
      tilt.current.style.transform = `perspective(900px) rotateY(${x * 24}deg) rotateX(${-y * 24}deg)`
    }
    window.addEventListener('mousemove', onMove)
    return () => window.removeEventListener('mousemove', onMove)
  }, [])

  return (
    <div className="rise" style={{ '--d': '.35s' }}>
      <div ref={tilt} className="tilt">
        <div className={`lens ${tag ? 'scan' : ''}`}>
          <div className="ring b" /><div className="ring" /><div className="ring c" />
          <div className="skin"><span className="mole" /><span className="beam" /></div>
          <div className="tags">
            {TAGS.map(([name, pos, dir], i) => (
              <button
                key={name} className={`tag ${dir} ${tag === name ? 'on' : ''}`}
                style={{ ...pos, '--d': `${i * 0.8}s` }}
                onMouseEnter={() => setTag(name)} onMouseLeave={() => setTag(null)}
                onFocus={() => setTag(name)} onBlur={() => setTag(null)}
              >{name}</button>
            ))}
          </div>
        </div>
      </div>
      <p key={tag} className="fade mx-auto mt-10 min-h-[3.5rem] max-w-xs text-center text-sm text-slate-300">
        {tag ? ABCDE[tag] : 'Hover a label to learn the ABCDE rule. Click anywhere to make sparks.'}
      </p>
    </div>
  )
}

export default function Landing({ onStart }) {
  // Magnetic button: leans toward the cursor
  const pull = (e) => {
    const r = e.currentTarget.getBoundingClientRect()
    e.currentTarget.style.transform = `translate(${(e.clientX - r.left - r.width / 2) * 0.25}px, ${(e.clientY - r.top - r.height / 2) * 0.35}px)`
  }
  const release = (e) => { e.currentTarget.style.transform = '' }

  return (
    <main className="relative z-10 min-h-screen overflow-hidden">
      <header className="mx-auto flex max-w-6xl items-center justify-between px-6 py-6 md:px-12">
        <span className="font-display text-2xl tracking-wide">DermAI</span>
        <span className="rounded-full border border-white/10 px-3 py-1 text-xs text-slate-300">
          Runs on your machine. Nothing leaves it.
        </span>
      </header>

      <section className="mx-auto grid max-w-6xl items-center gap-14 px-6 pb-20 pt-6 md:px-12 lg:grid-cols-[1.1fr_1fr] lg:pt-14">
        <div>
          <h1 className="font-display text-6xl leading-[.95] md:text-8xl">
            {'Look closer at that mole.'.split(' ').map((w, i) => (
              <span key={w} className="rise mr-[.22em] inline-block" style={{ '--d': `${0.1 + i * 0.1}s` }}>{w}</span>
            ))}
          </h1>
          <p className="rise mt-6 max-w-md text-lg leading-relaxed text-slate-300" style={{ '--d': '.7s' }}>
            Upload a photo or short video of a skin spot. A neural network trained on 10,015 dermoscopy
            images sorts it into one of 7 lesion types in seconds.
          </p>
          <div className="rise mt-9 flex flex-wrap items-center gap-5" style={{ '--d': '.85s' }}>
            <button className="cta text-base" onClick={onStart} onMouseMove={pull} onMouseLeave={release}>Scan a spot</button>
            <span className="text-sm text-slate-400">Takes about 5 seconds</span>
          </div>
          <p className="rise mt-12 max-w-md text-xs leading-relaxed text-slate-500" style={{ '--d': '1s' }}>
            Research prototype. It can’t replace a dermatologist. If a spot changes, bleeds or worries you, book a check-up.
          </p>
        </div>
        <Lens />
      </section>
    </main>
  )
}
