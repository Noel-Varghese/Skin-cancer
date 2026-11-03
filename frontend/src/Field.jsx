import { useEffect, useRef } from 'react'

// Particle network shared by every screen. Move the mouse to link up, click to burst.
export default function Field() {
  const ref = useRef(null)
  useEffect(() => {
    const c = ref.current
    const ctx = c.getContext('2d')
    const calm = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    const mouse = { x: -999, y: -999 }
    let w, h, raf, pts = []
    const dot = () => {
      const vx = (Math.random() - 0.5) * 0.35, vy = (Math.random() - 0.5) * 0.35
      return { vx, vy, bx: vx, by: vy }
    }
    const resize = () => {
      w = c.width = window.innerWidth; h = c.height = window.innerHeight
      pts = Array.from({ length: Math.min(80, Math.floor((w * h) / 20000)) }, () => ({ ...dot(), x: Math.random() * w, y: Math.random() * h }))
    }
    const move = (e) => {
      mouse.x = e.clientX; mouse.y = e.clientY
      const s = document.documentElement.style
      s.setProperty('--mx', e.clientX + 'px'); s.setProperty('--my', e.clientY + 'px')
    }
    const burst = (e) => {
      for (let i = 0; i < 10; i++) {
        const a = Math.random() * 6.283, s = 2 + Math.random() * 3
        pts.push({ ...dot(), x: e.clientX, y: e.clientY, vx: Math.cos(a) * s, vy: Math.sin(a) * s })
      }
      pts.splice(0, Math.max(0, pts.length - 130))
    }
    const tick = () => {
      ctx.clearRect(0, 0, w, h)
      for (const p of pts) {
        p.vx += (p.bx - p.vx) * 0.03; p.vy += (p.by - p.vy) * 0.03
        p.x += p.vx; p.y += p.vy
        if (p.x < 0 || p.x > w) { p.vx *= -1; p.bx *= -1 }
        if (p.y < 0 || p.y > h) { p.vy *= -1; p.by *= -1 }
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
    window.addEventListener('pointerdown', burst)
    return () => {
      cancelAnimationFrame(raf)
      window.removeEventListener('resize', resize)
      window.removeEventListener('mousemove', move)
      window.removeEventListener('pointerdown', burst)
    }
  }, [])
  return <canvas ref={ref} className="pointer-events-none fixed inset-0 opacity-70" aria-hidden="true" />
}
