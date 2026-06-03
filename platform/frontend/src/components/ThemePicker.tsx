import { Check, Plus } from "lucide-react";
import { ThemeSummary, themeBackgroundUrl } from "../api";

interface ThemePickerProps {
  themes: ThemeSummary[];
  selectedId: string | null;
  onSelect: (id: string) => void;
  onCreate: () => void;
}

export function ThemePicker({
  themes,
  selectedId,
  onSelect,
  onCreate,
}: ThemePickerProps) {
  return (
    <div className="theme-picker">
      <div className="theme-picker-grid">
        {themes.map((theme) => (
          <button
            key={theme.id}
            type="button"
            className={`theme-card ${selectedId === theme.id ? "selected" : ""}`}
            onClick={() => onSelect(theme.id)}
          >
            <div
              className="theme-card-preview"
              style={{
                backgroundImage: `url(${themeBackgroundUrl(theme.id, Date.now())})`,
              }}
            />
            <div className="theme-card-body">
              <span className="theme-card-name">{theme.name}</span>
              <span className="theme-card-meta">
                {theme.background_kind}
                {theme.is_builtin ? " · built-in" : ""}
              </span>
            </div>
            {selectedId === theme.id && (
              <span className="theme-card-check">
                <Check size={16} />
              </span>
            )}
          </button>
        ))}
        <button type="button" className="theme-card theme-card-new" onClick={onCreate}>
          <Plus size={28} />
          <span>Create theme</span>
        </button>
      </div>
    </div>
  );
}
