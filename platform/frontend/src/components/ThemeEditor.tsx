import { useEffect, useState } from "react";
import { Loader2, X } from "lucide-react";
import {
  PaletteSpec,
  ThemeDetail,
  TypographySpec,
  createTheme,
  getTheme,
  updateTheme,
} from "../api";

const DEFAULT_TYPO: TypographySpec = {
  heading: {
    font: "Inter",
    font_size: 48,
    color: "#FFFFFF",
    weight: "BOLD",
    cursor: "#FFFFFF",
  },
  subheading: {
    font: "Inter",
    font_size: 36,
    color: "#FFFFFF",
    weight: "BOLD",
    cursor: "#FFEB3B",
  },
  paragraph: {
    font: "Inter",
    font_size: 28,
    color: "#000000",
    weight: "BOLD",
    cursor: "#FFEB3B",
  },
  code: {
    font: "Courier New",
    font_size: 22,
    color: "#abb2bf",
    weight: "NORMAL",
    cursor: null,
  },
};

interface ThemeEditorProps {
  themeId?: string | null;
  onClose: () => void;
  onSaved: (themeId?: string) => void;
}

type TypographyStyle = TypographySpec["heading"];

export function ThemeEditor({ themeId, onClose, onSaved }: ThemeEditorProps) {
  const [loading, setLoading] = useState(Boolean(themeId));
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [stylePack, setStylePack] = useState("course_clean");
  const [backgroundLoop, setBackgroundLoop] = useState(true);
  const [typography, setTypography] = useState<TypographySpec>(DEFAULT_TYPO);
  const [palette, setPalette] = useState<PaletteSpec>({
    card_fill: "#FFFFFF",
    card_stroke: "#888888",
    accent: "#FFEB3B",
    emphasis_red: "#FC6255",
    label_color: "#FFEB3B",
    code_bg: "#282c34",
    code_text: "#abb2bf",
  });
  const [backgroundFile, setBackgroundFile] = useState<File | null>(null);
  const [isBuiltin, setIsBuiltin] = useState(false);

  useEffect(() => {
    if (!themeId) return;
    setLoading(true);
    getTheme(themeId)
      .then((t: ThemeDetail) => {
        setName(t.name);
        setDescription(t.description);
        setStylePack(t.style_pack);
        setBackgroundLoop(t.background_loop);
        setTypography(t.typography);
        if (t.palette) setPalette(t.palette);
        setIsBuiltin(t.is_builtin);
      })
      .catch((e) => setError(String(e)))
      .finally(() => setLoading(false));
  }, [themeId]);

  const handleSave = async () => {
    if (!name.trim()) {
      setError("Theme name is required");
      return;
    }
    setSaving(true);
    setError(null);
    const form = new FormData();
    form.append("name", name.trim());
    form.append("description", description);
    form.append("style_pack", stylePack);
    form.append("background_loop", String(backgroundLoop));
    form.append("typography_json", JSON.stringify(typography));
    form.append("palette_json", JSON.stringify(palette));
    if (backgroundFile) form.append("background", backgroundFile);
    try {
      if (themeId) {
        await updateTheme(themeId, form);
        onSaved(themeId);
      } else {
        if (!backgroundFile) {
          setError("Upload a background image, GIF, or video");
          setSaving(false);
          return;
        }
        const created = await createTheme(form);
        onSaved(created.id);
      }
      onClose();
    } catch (e) {
      setError(String(e));
    } finally {
      setSaving(false);
    }
  };

  const typoField = (
    role: keyof TypographySpec,
    label: string,
    fields: (keyof TypographySpec["heading"])[] = ["font_size", "color", "font"]
  ) => (
    <div className="theme-editor-section">
      <div className="theme-editor-section-title">{label}</div>
      <div className="theme-editor-row">
        {fields.map((field) => (
          <label key={field} className="theme-editor-field">
            <span>{field.replace("_", " ")}</span>
            <input
              type={field === "font_size" ? "number" : "text"}
              value={String(typography[role][field as keyof TypographyStyle] ?? "")}
              onChange={(e) =>
                setTypography({
                  ...typography,
                  [role]: {
                    ...typography[role],
                    [field]:
                      field === "font_size"
                        ? Number(e.target.value)
                        : e.target.value,
                  },
                })
              }
            />
          </label>
        ))}
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="theme-editor-overlay">
        <div className="theme-editor">
          <Loader2 className="spin" size={32} />
        </div>
      </div>
    );
  }

  return (
    <div className="theme-editor-overlay">
      <div className="theme-editor">
        <div className="theme-editor-header">
          <h2>{themeId ? "Edit theme" : "Create theme"}</h2>
          <button type="button" className="btn-ghost sm" onClick={onClose}>
            <X size={18} />
          </button>
        </div>

        {error && <div className="error-bar">{error}</div>}

        <label className="theme-editor-field full">
          <span>Name</span>
          <input value={name} onChange={(e) => setName(e.target.value)} disabled={isBuiltin} />
        </label>

        <label className="theme-editor-field full">
          <span>Description</span>
          <input value={description} onChange={(e) => setDescription(e.target.value)} />
        </label>

        <label className="theme-editor-field full">
          <span>Style pack (icons)</span>
          <select value={stylePack} onChange={(e) => setStylePack(e.target.value)}>
            <option value="course_clean">course_clean</option>
            <option value="playful">playful</option>
          </select>
        </label>

        {!isBuiltin && (
          <label className="theme-editor-field full">
            <span>Background (PNG, JPG, GIF, MP4)</span>
            <input
              type="file"
              accept="image/*,video/mp4,video/webm"
              onChange={(e) => setBackgroundFile(e.target.files?.[0] ?? null)}
            />
          </label>
        )}

        <label className="theme-editor-checkbox">
          <input
            type="checkbox"
            checked={backgroundLoop}
            onChange={(e) => setBackgroundLoop(e.target.checked)}
          />
          Loop GIF / video background
        </label>

        {typoField("heading", "Heading (labels)")}
        {typoField("subheading", "Subheading (on background text)")}
        {typoField("paragraph", "Paragraph (card text)")}
        {typoField("code", "Code", ["font", "font_size", "color"])}

        <div className="theme-editor-section">
          <div className="theme-editor-section-title">Color palette</div>
          <div className="theme-editor-row">
            {(["card_fill", "accent", "code_bg", "code_text"] as const).map((key) => (
              <label key={key} className="theme-editor-field">
                <span>{key.replace("_", " ")}</span>
                <input
                  type="text"
                  value={palette[key]}
                  onChange={(e) => setPalette({ ...palette, [key]: e.target.value })}
                />
              </label>
            ))}
          </div>
        </div>

        <div className="theme-editor-actions">
          <button type="button" className="btn-ghost" onClick={onClose}>
            Cancel
          </button>
          <button type="button" className="btn-primary" disabled={saving} onClick={handleSave}>
            {saving ? <Loader2 size={16} className="spin" /> : null}
            Save theme
          </button>
        </div>
      </div>
    </div>
  );
}
