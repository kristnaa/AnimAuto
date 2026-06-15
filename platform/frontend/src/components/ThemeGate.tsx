import { useEffect, useState } from "react";
import { Film, Loader2, Mic, Palette } from "lucide-react";
import { CreationMode, ThemeSummary, createProject, listThemes } from "../api";
import { ThemeEditor } from "./ThemeEditor";
import { ThemePicker } from "./ThemePicker";

interface ThemeGateProps {
  onReady: (projectId: string) => void;
  onBack?: () => void;
}

type GateMode = "beat_studio" | "voice_motion";

export function ThemeGate({ onReady, onBack }: ThemeGateProps) {
  const [gateMode, setGateMode] = useState<GateMode>("beat_studio");
  const [themes, setThemes] = useState<ThemeSummary[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>("builtin_orange");
  const [projectName, setProjectName] = useState("My Animation");
  const [loading, setLoading] = useState(true);
  const [starting, setStarting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [editorOpen, setEditorOpen] = useState(false);
  const [editThemeId, setEditThemeId] = useState<string | null>(null);

  const refreshThemes = () => {
    return listThemes()
      .then((res) => {
        setThemes(res.themes);
        if (!selectedId && res.themes.length) {
          setSelectedId(res.themes[0].id);
        }
      })
      .catch((e) => setError(String(e)));
  };

  useEffect(() => {
    refreshThemes().finally(() => setLoading(false));
  }, []);

  const handleContinue = async () => {
    if (gateMode === "beat_studio" && !selectedId) {
      setError("Select a theme to continue");
      return;
    }
    setStarting(true);
    setError(null);
    try {
      const creationMode: CreationMode = gateMode === "voice_motion" ? "voice_motion" : "beat_studio";
      const themeId = gateMode === "voice_motion" ? "builtin_orange" : selectedId!;
      const project = await createProject(
        projectName.trim() || "My Animation",
        themeId,
        creationMode
      );
      onReady(project.id);
    } catch (e) {
      setError(String(e));
    } finally {
      setStarting(false);
    }
  };

  if (loading) {
    return (
      <div className="theme-gate">
        <Loader2 size={40} className="spin" />
      </div>
    );
  }

  return (
    <div className="theme-gate">
      <div className="theme-gate-inner">
        <div className="theme-gate-brand">
          <Film size={28} />
          <h1>Manimations Studio</h1>
          {onBack && (
            <button type="button" className="btn-ghost sm theme-gate-back" onClick={onBack}>
              ← All projects
            </button>
          )}
        </div>

        <div className="creation-mode-grid">
          <button
            type="button"
            className={`creation-mode-card ${gateMode === "beat_studio" ? "active" : ""}`}
            onClick={() => setGateMode("beat_studio")}
          >
            <Palette size={22} />
            <strong>Beat studio</strong>
            <span>Themed slides with cards, icons, and beat scripts</span>
          </button>
          <button
            type="button"
            className={`creation-mode-card ${gateMode === "voice_motion" ? "active" : ""}`}
            onClick={() => setGateMode("voice_motion")}
          >
            <Mic size={22} />
            <strong>Voice motion</strong>
            <span>Upload narration → Manim shapes on black — no cards or icons</span>
          </button>
        </div>

        {gateMode === "beat_studio" ? (
          <>
            <p className="theme-gate-lead">
              Choose a visual theme for your video — background, typography, and colors.
            </p>
            <ThemePicker
              themes={themes}
              selectedId={selectedId}
              onSelect={setSelectedId}
              onCreate={() => {
                setEditThemeId(null);
                setEditorOpen(true);
              }}
            />
          </>
        ) : (
          <p className="theme-gate-lead">
            Black canvas, white text, colorful Manim shapes synced to your uploaded voice.
            No theme or beat templates required.
          </p>
        )}

        {error && <div className="error-bar">{error}</div>}

        <label className="theme-gate-name">
          <span>Project name</span>
          <input
            value={projectName}
            onChange={(e) => setProjectName(e.target.value)}
            placeholder="My Animation"
          />
        </label>

        <button
          type="button"
          className="btn-primary theme-gate-continue"
          disabled={(gateMode === "beat_studio" && !selectedId) || starting}
          onClick={handleContinue}
        >
          {starting ? <Loader2 size={18} className="spin" /> : null}
          Continue to Studio
        </button>
      </div>

      {editorOpen && (
        <ThemeEditor
          themeId={editThemeId}
          onClose={() => setEditorOpen(false)}
          onSaved={(newThemeId) => {
            refreshThemes().then(() => {
              if (newThemeId) setSelectedId(newThemeId);
            });
          }}
        />
      )}
    </div>
  );
}
