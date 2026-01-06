import { useEffect, useRef } from "react";

type Star = {
  x: number;
  y: number;
  speed: number;
  length: number;
  opacity: number;
};

export default function StarBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const resize = () => {
      const dpr = window.devicePixelRatio || 1;
      canvas.width = window.innerWidth * dpr;
      canvas.height = window.innerHeight * dpr;
      canvas.style.width = `${window.innerWidth}px`;
      canvas.style.height = `${window.innerHeight}px`;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };

    resize();
    window.addEventListener("resize", resize);

    const STAR_COUNT = 70;
    const ANGLE = Math.PI / 4.2; // cinematic diagonal

    const spawnStar = (initial = false): Star => {
      if (initial) {
        return {
          x: Math.random() * window.innerWidth,
          y: Math.random() * window.innerHeight,
          speed: Math.random() * 1.2 + 0.9,
          length: Math.random() * 45 + 25,
          opacity: Math.random() * 0.5 + 0.4,
        };
      }

      // Spawn from top OR left OR right (balanced)
      const edge = Math.random();

      if (edge < 0.33) {
        return {
          x: Math.random() * window.innerWidth,
          y: -120,
          speed: Math.random() * 1.2 + 0.9,
          length: Math.random() * 45 + 25,
          opacity: Math.random() * 0.5 + 0.4,
        };
      }

      if (edge < 0.66) {
        return {
          x: -120,
          y: Math.random() * window.innerHeight,
          speed: Math.random() * 1.2 + 0.9,
          length: Math.random() * 45 + 25,
          opacity: Math.random() * 0.5 + 0.4,
        };
      }

      return {
        x: window.innerWidth + 120,
        y: Math.random() * window.innerHeight,
        speed: Math.random() * 1.2 + 0.9,
        length: Math.random() * 45 + 25,
        opacity: Math.random() * 0.5 + 0.4,
      };
    };

    const stars: Star[] = Array.from(
      { length: STAR_COUNT },
      () => spawnStar(true)
    );

    let frameId: number;

    const animate = () => {
      ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);

      for (let i = 0; i < stars.length; i++) {
        const s = stars[i];

        const dx = Math.cos(ANGLE) * s.speed;
        const dy = Math.sin(ANGLE) * s.speed;

        ctx.beginPath();
        ctx.moveTo(s.x, s.y);
        ctx.lineTo(
          s.x - dx * (s.length / s.speed),
          s.y - dy * (s.length / s.speed)
        );

        ctx.strokeStyle = `rgba(255,255,255,${s.opacity})`;
        ctx.lineWidth = 1.4;
        ctx.lineCap = "round";
        ctx.shadowBlur = 8;
        ctx.shadowColor = "rgba(255,255,255,0.6)";
        ctx.stroke();
        ctx.shadowBlur = 0;

        s.x += dx;
        s.y += dy;

        if (
          s.x > window.innerWidth + 200 ||
          s.y > window.innerHeight + 200
        ) {
          stars[i] = spawnStar(false);
        }
      }

      frameId = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      window.removeEventListener("resize", resize);
      cancelAnimationFrame(frameId);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 z-0 pointer-events-none"
    />
  );
}
