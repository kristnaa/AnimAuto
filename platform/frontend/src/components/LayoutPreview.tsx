import type { BeatTypeRegion } from "../api";

const KIND_COLORS: Record<string, { fill: string; stroke: string }> = {
  label: { fill: "rgba(139, 92, 246, 0.22)", stroke: "rgba(139, 92, 246, 0.65)" },
  card: { fill: "rgba(250, 250, 250, 0.12)", stroke: "rgba(250, 250, 250, 0.35)" },
  icon: { fill: "rgba(245, 158, 11, 0.18)", stroke: "rgba(245, 158, 11, 0.55)" },
  text: { fill: "rgba(96, 165, 250, 0.15)", stroke: "rgba(96, 165, 250, 0.45)" },
  code: { fill: "rgba(40, 44, 52, 0.95)", stroke: "rgba(62, 68, 81, 0.9)" },
  output: { fill: "rgba(33, 37, 43, 0.95)", stroke: "rgba(62, 68, 81, 0.9)" },
};

interface LayoutPreviewProps {
  title: string;
  layout: string;
  regions: BeatTypeRegion[];
  compact?: boolean;
}

export function LayoutPreview({ title, layout, regions, compact }: LayoutPreviewProps) {
  const w = compact ? 160 : 220;
  const h = compact ? 100 : 140;

  return (
    <div className={`layout-preview ${compact ? "layout-preview-compact" : ""}`}>
      <div className="layout-preview-header">
        <span className="layout-preview-title">{title}</span>
        <span className="layout-preview-layout">{layout}</span>
      </div>
      <svg
        viewBox="0 0 1 1"
        width={w}
        height={h}
        className="layout-preview-svg"
        aria-label={`Layout preview: ${layout}`}
      >
        <rect
          x={0.02}
          y={0.02}
          width={0.96}
          height={0.96}
          rx={0.03}
          fill="rgba(255,255,255,0.03)"
          stroke="rgba(255,255,255,0.12)"
          strokeWidth={0.01}
        />
        {regions.map((r) => {
          const colors = KIND_COLORS[r.kind] ?? KIND_COLORS.card;
          return (
            <g key={r.id}>
              <rect
                x={r.x}
                y={r.y}
                width={r.w}
                height={r.h}
                rx={0.015}
                fill={colors.fill}
                stroke={colors.stroke}
                strokeWidth={0.008}
              />
              <text
                x={r.x + r.w / 2}
                y={r.y + r.h / 2}
                textAnchor="middle"
                dominantBaseline="middle"
                fill="rgba(255,255,255,0.75)"
                fontSize={0.045}
                fontFamily="Inter, system-ui, sans-serif"
              >
                {r.label}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}
