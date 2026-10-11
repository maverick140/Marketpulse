import React, { useEffect, useRef, useState } from 'react';

export interface CandlePoint {
  time: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume?: number;
}

interface Props {
  data: CandlePoint[];
  height?: number;
}

export const CandlestickChart: React.FC<Props> = ({ data, height = 320 }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [width, setWidth] = useState(600);
  const [hoverIndex, setHoverIndex] = useState<number | null>(null);

  useEffect(() => {
    const handleResize = () => {
      if (containerRef.current) {
        setWidth(containerRef.current.clientWidth);
      }
    };

    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  if (!data || data.length === 0) {
    return (
      <div
        style={{
          height: `${height}px`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: '#64748b',
          fontSize: '0.875rem',
        }}
      >
        No historical candle data available
      </div>
    );
  }

  // Calculate price bounds with 5% padding
  const allLows = data.map((d) => d.low);
  const allHighs = data.map((d) => d.high);
  const rawMin = Math.min(...allLows);
  const rawMax = Math.max(...allHighs);
  const spread = rawMax - rawMin || rawMax * 0.02 || 1;
  const minPrice = rawMin - spread * 0.05;
  const maxPrice = rawMax + spread * 0.05;

  const marginTop = 15;
  const marginBottom = 28;
  const marginLeft = 15;
  const marginRight = 65;

  const plotWidth = Math.max(100, width - marginLeft - marginRight);
  const plotHeight = Math.max(80, height - marginTop - marginBottom);

  const getY = (price: number) => {
    const ratio = (price - minPrice) / (maxPrice - minPrice);
    return marginTop + (1 - ratio) * plotHeight;
  };

  const slotWidth = plotWidth / data.length;
  const candleBodyWidth = Math.max(3, Math.min(16, slotWidth * 0.72));

  // Generate 5 horizontal grid levels
  const gridLevels = [0, 0.25, 0.5, 0.75, 1].map((frac) => {
    const price = minPrice + frac * (maxPrice - minPrice);
    const y = getY(price);
    return { price, y };
  });

  // Pick 5-6 date ticks evenly spaced
  const tickStep = Math.max(1, Math.floor(data.length / 5));
  const dateTicks: { index: number; label: string; x: number }[] = [];
  for (let i = 0; i < data.length; i += tickStep) {
    dateTicks.push({
      index: i,
      label: data[i].time,
      x: marginLeft + (i + 0.5) * slotWidth,
    });
  }

  const handleMouseMove = (e: React.MouseEvent<SVGSVGElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const mouseX = e.clientX - rect.left - marginLeft;
    if (mouseX >= 0 && mouseX <= plotWidth) {
      const idx = Math.floor(mouseX / slotWidth);
      if (idx >= 0 && idx < data.length) {
        setHoverIndex(idx);
      }
    }
  };

  const handleMouseLeave = () => {
    setHoverIndex(null);
  };

  const activeCandle = hoverIndex !== null ? data[hoverIndex] : null;
  const activeChange = activeCandle ? activeCandle.close - activeCandle.open : 0;
  const activeChangePct = activeCandle && activeCandle.open ? (activeChange / activeCandle.open) * 100 : 0;
  const activeIsBullish = activeChange >= 0;

  return (
    <div ref={containerRef} style={{ width: '100%', height: `${height}px`, position: 'relative' }}>
      {/* Floating or Top Tooltip Banner */}
      {activeCandle && (
        <div
          style={{
            position: 'absolute',
            top: '4px',
            left: `${marginLeft}px`,
            right: `${marginRight}px`,
            display: 'flex',
            gap: '1rem',
            alignItems: 'center',
            flexWrap: 'wrap',
            padding: '0.35rem 0.65rem',
            backgroundColor: 'rgba(15, 23, 42, 0.85)',
            border: '1px solid #1e293b',
            borderRadius: '6px',
            fontSize: '0.75rem',
            fontFamily: 'var(--font-mono)',
            zIndex: 10,
            pointerEvents: 'none',
          }}
        >
          <span style={{ color: '#94a3b8', fontWeight: 600 }}>{activeCandle.time}</span>
          <span>
            <strong style={{ color: '#64748b' }}>O: </strong>₹{activeCandle.open.toFixed(2)}
          </span>
          <span>
            <strong style={{ color: '#64748b' }}>H: </strong>₹{activeCandle.high.toFixed(2)}
          </span>
          <span>
            <strong style={{ color: '#64748b' }}>L: </strong>₹{activeCandle.low.toFixed(2)}
          </span>
          <span>
            <strong style={{ color: '#64748b' }}>C: </strong>₹{activeCandle.close.toFixed(2)}
          </span>
          <span style={{ color: activeIsBullish ? '#34d399' : '#f87171', fontWeight: 700 }}>
            {activeIsBullish ? '+' : ''}{activeChangePct.toFixed(2)}% ({activeIsBullish ? '+' : ''}{activeChange.toFixed(2)})
          </span>
          {activeCandle.volume !== undefined && activeCandle.volume > 0 && (
            <span style={{ color: '#64748b', marginLeft: 'auto' }}>
              Vol: {activeCandle.volume.toLocaleString()}
            </span>
          )}
        </div>
      )}

      <svg
        width={width}
        height={height}
        onMouseMove={handleMouseMove}
        onMouseLeave={handleMouseLeave}
        style={{ display: 'block', overflow: 'visible', cursor: 'crosshair' }}
      >
        {/* Horizontal Gridlines and Right Price Labels */}
        {gridLevels.map((lvl, idx) => (
          <g key={idx}>
            <line
              x1={marginLeft}
              y1={lvl.y}
              x2={width - marginRight}
              y2={lvl.y}
              stroke="#1e293b"
              strokeDasharray="3 3"
              strokeWidth={1}
            />
            <text
              x={width - marginRight + 6}
              y={lvl.y + 4}
              fill="#64748b"
              fontSize={11}
              fontFamily="var(--font-mono)"
              textAnchor="start"
            >
              ₹{lvl.price.toFixed(lvl.price >= 1000 ? 0 : 2)}
            </text>
          </g>
        ))}

        {/* X-axis Date Labels */}
        {dateTicks.map((tick, idx) => (
          <text
            key={idx}
            x={tick.x}
            y={height - 8}
            fill="#64748b"
            fontSize={11}
            textAnchor="middle"
          >
            {tick.label}
          </text>
        ))}

        {/* Candlesticks */}
        {data.map((d, i) => {
          const x = marginLeft + (i + 0.5) * slotWidth;
          const isBull = d.close >= d.open;
          const color = isBull ? '#10b981' : '#f43f5e';
          const yHigh = getY(d.high);
          const yLow = getY(d.low);
          const yOpen = getY(d.open);
          const yClose = getY(d.close);
          const bodyTop = Math.min(yOpen, yClose);
          const bodyHeight = Math.max(2, Math.abs(yOpen - yClose));

          return (
            <g key={i}>
              {/* Upper & Lower Wick */}
              <line
                x1={x}
                y1={yHigh}
                x2={x}
                y2={yLow}
                stroke={color}
                strokeWidth={1.5}
                strokeLinecap="round"
              />
              {/* Candle Body */}
              <rect
                x={x - candleBodyWidth / 2}
                y={bodyTop}
                width={candleBodyWidth}
                height={bodyHeight}
                fill={color}
                rx={1}
              />
            </g>
          );
        })}

        {/* Hover Crosshair */}
        {hoverIndex !== null && (
          <line
            x1={marginLeft + (hoverIndex + 0.5) * slotWidth}
            y1={marginTop}
            x2={marginLeft + (hoverIndex + 0.5) * slotWidth}
            y2={height - marginBottom}
            stroke="#64748b"
            strokeDasharray="2 2"
            strokeWidth={1}
            pointerEvents="none"
          />
        )}
      </svg>
    </div>
  );
};
