import { useEffect, useState } from "react";
import { LayoutGrid } from "lucide-react";
import type { BeatTypeLayoutVariant, BeatTypeMeta } from "../api";
import { LayoutPreview } from "./LayoutPreview";

function pickLayoutVariant(
  beatType: BeatTypeMeta | undefined,
  preferredLayoutId?: string | null,
): BeatTypeLayoutVariant | null {
  const variants = beatType?.layout_variants;
  if (!variants?.length) return null;
  if (preferredLayoutId) {
    const match = variants.find(
      (v) => v.id === preferredLayoutId || v.layout === preferredLayoutId,
    );
    if (match) return match;
  }
  return variants[0];
}

interface BeatTypePickerProps {
  beatTypes: BeatTypeMeta[];
  selectedId: string | null;
  /** LAYOUT line from the active ### BEAT block in the script editor. */
  detectedLayoutId?: string | null;
  onSelect: (beatType: BeatTypeMeta) => void;
  onInsertTemplate: (beatType: BeatTypeMeta, layoutVariant?: BeatTypeLayoutVariant) => void;
  onLayoutVariantChange?: (layoutVariant: BeatTypeLayoutVariant | null) => void;
}

export function BeatTypePicker({
  beatTypes,
  selectedId,
  detectedLayoutId,
  onSelect,
  onInsertTemplate,
  onLayoutVariantChange,
}: BeatTypePickerProps) {
  const active = beatTypes.find((b) => b.id === selectedId) ?? beatTypes[0];
  const variants = active?.layout_variants ?? [];
  const [manualLayoutId, setManualLayoutId] = useState<string | null>(null);

  useEffect(() => {
    setManualLayoutId(null);
  }, [active?.id]);

  const activeLayout = pickLayoutVariant(active, manualLayoutId ?? detectedLayoutId);

  useEffect(() => {
    onLayoutVariantChange?.(activeLayout);
  }, [activeLayout?.id, onLayoutVariantChange]);

  const previewLayout = activeLayout?.layout ?? active?.layout ?? "";
  const previewRegions = activeLayout?.regions ?? active?.regions ?? [];
  const previewTitle = activeLayout ? `${active?.label} · ${activeLayout.label}` : active?.label ?? "";
  const previewDesc = activeLayout?.description ?? active?.description ?? "";

  return (
    <div className="beat-type-picker">
      <div className="beat-type-picker-head">
        <LayoutGrid size={14} />
        <span>Beat type</span>
      </div>
      <div className="beat-type-grid">
        {beatTypes.map((bt) => (
          <button
            key={bt.id}
            type="button"
            className={`beat-type-chip ${selectedId === bt.id ? "active" : ""}`}
            onClick={() => onSelect(bt)}
            title={bt.description}
          >
            {bt.label}
          </button>
        ))}
      </div>
      {active && (
        <div className="beat-type-detail">
          {variants.length > 0 && (
            <div className="beat-layout-variants">
              <span className="beat-layout-variants-label">Statement layout</span>
              <div className="beat-type-grid">
                {variants.map((variant) => (
                  <button
                    key={variant.id}
                    type="button"
                    className={`beat-type-chip beat-layout-chip ${
                      activeLayout?.id === variant.id ? "active" : ""
                    }`}
                    onClick={() => setManualLayoutId(variant.id)}
                    title={variant.description}
                  >
                    {variant.label}
                  </button>
                ))}
              </div>
            </div>
          )}
          <LayoutPreview
            title={previewTitle}
            layout={previewLayout}
            regions={previewRegions}
          />
          <p className="beat-type-desc">{previewDesc}</p>
          <button
            type="button"
            className="btn-ghost sm beat-type-insert"
            onClick={() => onInsertTemplate(active, activeLayout ?? undefined)}
          >
            Insert template block
          </button>
        </div>
      )}
    </div>
  );
}
