import { LayoutGrid } from "lucide-react";
import type { BeatTypeMeta } from "../api";
import { LayoutPreview } from "./LayoutPreview";

interface BeatTypePickerProps {
  beatTypes: BeatTypeMeta[];
  selectedId: string | null;
  onSelect: (beatType: BeatTypeMeta) => void;
  onInsertTemplate: (beatType: BeatTypeMeta) => void;
}

export function BeatTypePicker({
  beatTypes,
  selectedId,
  onSelect,
  onInsertTemplate,
}: BeatTypePickerProps) {
  const active = beatTypes.find((b) => b.id === selectedId) ?? beatTypes[0];

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
          <LayoutPreview
            title={active.label}
            layout={active.layout}
            regions={active.regions}
          />
          <p className="beat-type-desc">{active.description}</p>
          <button
            type="button"
            className="btn-ghost sm beat-type-insert"
            onClick={() => onInsertTemplate(active)}
          >
            Insert template block
          </button>
        </div>
      )}
    </div>
  );
}
