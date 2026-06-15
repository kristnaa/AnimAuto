import { useCallback, useState } from "react";
import { Check, Film, Loader2, Sparkles } from "lucide-react";
import type { DirectorPage, Project, VoiceMotionData } from "../api";
import {
  approveVoiceStoryboard,
  generateVoiceMotion,
  generateVoiceStoryboard,
  patchVoiceStoryboard,
} from "../api";

const LAYOUT_LABELS: Record<string, string> = {
  center_title: "Hook title",
  center_bullets: "Bullet list",
  flowchart_vertical: "Flowchart ↓",
  flowchart_horizontal: "Flowchart →",
  compare_columns: "Compare columns",
  diagram_labeled: "Concept diagram",
  kinetic_keywords: "Keyword pulse",
  visual_orbit: "Orbit hub",
  pipeline_blackboard: "Blackboard pipeline",
  mind_map_radial: "Mind map radial",
  fade_transition: "Transition",
};

const BACKGROUND_LABELS: Record<string, string> = {
  blackboard_clean: "Blackboard clean",
  radial_blue: "Radial blue",
  corner_warm: "Warm corners",
  grid_fade: "Grid teal",
  split_tone: "Split tone",
  orbit_glow: "Orbit glow",
  edge_frame: "Edge frame",
};

function onScreenPreview(page: DirectorPage): string {
  const parts: string[] = [];
  if (page.headline) parts.push(page.headline);
  if (page.keyword) parts.push(`「${page.keyword}」`);
  if (page.bullets?.length) parts.push(page.bullets.join(" · "));
  if (page.flow_labels?.length) parts.push(page.flow_labels.join(" → "));
  if (page.stages?.length) {
    parts.push(
      page.stages.map((s) => `${s.icon_id ?? "?"}:${s.label}`).join(" → ")
    );
  }
  if (page.branches?.length) {
    const mode = page.mode ?? "single";
    parts.push(
      `[${mode}] ${page.branches.map((b) => `${b.icon_id ?? "?"}:${b.label}`).join(mode === "full" ? " · " : "")}`
    );
    if (page.hub_label) parts.unshift(`hub:${page.hub_label}`);
  }
  if (page.hub_label && !page.branches?.length) parts.push(`hub: ${page.hub_label}`);
  if (page.orbit_labels?.length) parts.push(page.orbit_labels.join(" · "));
  if (page.left_label && page.right_label) parts.push(`${page.left_label} vs ${page.right_label}`);
  if (page.shape_label) parts.push(page.shape_label);
  if (page.hint) parts.push(page.hint);
  return parts.join(" | ") || "(visual only)";
}

interface VoiceStoryboardPanelProps {
  projectId: string;
  voiceMotion: VoiceMotionData | null | undefined;
  onProjectUpdate: (project: Project) => void;
  onCodeGenerated: (code: string) => void;
  onGenerateVideo: () => Promise<void>;
  disabled?: boolean;
}

function formatTime(sec: number): string {
  const m = Math.floor(sec / 60);
  const s = Math.floor(sec % 60);
  return `${m}:${s.toString().padStart(2, "0")}`;
}

export function VoiceStoryboardPanel({
  projectId,
  voiceMotion,
  onProjectUpdate,
  onCodeGenerated,
  onGenerateVideo,
  disabled,
}: VoiceStoryboardPanelProps) {
  const [busy, setBusy] = useState<"storyboard" | "patch" | "approve" | "video" | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [localPages, setLocalPages] = useState<DirectorPage[] | null>(null);

  const plan = voiceMotion?.director_plan;
  const pages = localPages ?? plan?.pages ?? [];
  const hasStoryboard = pages.length > 0;
  const isApproved = voiceMotion?.storyboard_status === "approved";
  const warnings = voiceMotion?.storyboard_warnings ?? [];

  const syncPages = useCallback(
    async (nextPages: DirectorPage[]) => {
      setBusy("patch");
      setError(null);
      try {
        const res = await patchVoiceStoryboard(projectId, nextPages);
        setLocalPages(res.director_plan.pages);
        onProjectUpdate(res.project);
      } catch (e) {
        setError(String(e));
      } finally {
        setBusy(null);
      }
    },
    [projectId, onProjectUpdate]
  );

  const handleGenerateStoryboard = async () => {
    setBusy("storyboard");
    setError(null);
    setLocalPages(null);
    try {
      const res = await generateVoiceStoryboard(projectId);
      setLocalPages(res.director_plan.pages);
      onProjectUpdate(res.project);
    } catch (e) {
      setError(String(e));
    } finally {
      setBusy(null);
    }
  };

  const handleLayoutChange = (index: number, layout: string) => {
    const next = pages.map((p, i) => (i === index ? { ...p, layout } : p));
    setLocalPages(next);
    void syncPages(next);
  };

  const handleHeadlineChange = (index: number, headline: string) => {
    const next = pages.map((p, i) => (i === index ? { ...p, headline } : p));
    setLocalPages(next);
  };

  const handleHeadlineBlur = () => {
    if (!localPages) return;
    void syncPages(localPages);
  };

  const handleApproveAndGenerate = async () => {
    setBusy("approve");
    setError(null);
    try {
      let project: Project;
      if (!isApproved) {
        const res = await approveVoiceStoryboard(projectId);
        project = res.project;
        onProjectUpdate(project);
      } else {
        project = { id: projectId } as Project;
      }
      setBusy("video");
      const gen = await generateVoiceMotion(projectId);
      onProjectUpdate(gen.project);
      onCodeGenerated(gen.code);
      await onGenerateVideo();
    } catch (e) {
      setError(String(e));
    } finally {
      setBusy(null);
    }
  };

  const hasAudio = Boolean(voiceMotion?.audio_ref);

  return (
    <div className="voice-storyboard-panel">
      <div className="voice-storyboard-toolbar">
        <button
          type="button"
          className="btn-secondary sm"
          onClick={handleGenerateStoryboard}
          disabled={disabled || !hasAudio || busy !== null}
          title="Transcribe audio and design one page per sentence"
        >
          {busy === "storyboard" ? (
            <Loader2 size={14} className="spin" />
          ) : (
            <Sparkles size={14} />
          )}
          Generate storyboard
        </button>
        {hasStoryboard && (
          <button
            type="button"
            className="btn-primary sm"
            onClick={handleApproveAndGenerate}
            disabled={disabled || busy !== null}
            title="Approve storyboard, compile Manim scene, and render preview"
          >
            {busy === "approve" || busy === "video" ? (
              <Loader2 size={14} className="spin" />
            ) : isApproved ? (
              <Film size={14} />
            ) : (
              <Check size={14} />
            )}
            {isApproved ? "Generate video" : "Approve & generate video"}
          </button>
        )}
        {hasStoryboard && (
          <span className={`voice-storyboard-status ${isApproved ? "approved" : "draft"}`}>
            {isApproved ? "Approved" : "Draft — review layouts"}
          </span>
        )}
      </div>

      {warnings.length > 0 && (
        <ul className="voice-storyboard-warnings">
          {warnings.map((w, i) => (
            <li key={i}>{w}</li>
          ))}
        </ul>
      )}

      {error && <div className="error-bar compact">{error}</div>}

      {hasStoryboard && plan?.summary && (
        <p className="voice-storyboard-summary">{plan.summary}</p>
      )}

      {hasStoryboard && (
        <ol className="voice-storyboard-list">
          {pages.map((page, i) => (
            <li key={page.id || i} className="voice-storyboard-item">
              <div className="voice-storyboard-item-head">
                <span className="voice-segment-time">
                  {formatTime(page.start)}–{formatTime(page.end)}
                </span>
                <span className="voice-segment-text voice-narration-line">
                  {page.sentence_text ? `🎙 ${page.sentence_text}` : "—"}
                </span>
              </div>
              <div className="voice-storyboard-on-screen">
                <span className="voice-storyboard-on-screen-label">On screen</span>
                {onScreenPreview(page)}
                {page.background_style && (
                  <span className="voice-storyboard-bg-badge">
                    {BACKGROUND_LABELS[page.background_style] ?? page.background_style}
                  </span>
                )}
              </div>
              <div className="voice-storyboard-item-controls">
                <label className="voice-storyboard-layout-label">
                  Layout
                  <select
                    value={page.layout}
                    onChange={(e) => handleLayoutChange(i, e.target.value)}
                    disabled={disabled || busy === "patch"}
                  >
                    {Object.entries(LAYOUT_LABELS).map(([id, label]) => (
                      <option key={id} value={id}>
                        {label}
                      </option>
                    ))}
                  </select>
                </label>
                {(page.layout === "center_title" || page.headline) && (
                  <label className="voice-storyboard-headline-label">
                    Hook (≤4 words)
                    <input
                      type="text"
                      value={page.headline ?? ""}
                      onChange={(e) => handleHeadlineChange(i, e.target.value)}
                      onBlur={handleHeadlineBlur}
                      disabled={disabled || busy === "patch"}
                      placeholder="Short hook"
                    />
                  </label>
                )}
              </div>
            </li>
          ))}
        </ol>
      )}

      {hasAudio && !hasStoryboard && (
        <p className="voiceover-hint">
          Click <strong>Generate storyboard</strong> to transcribe your narration and design one
          animated page per sentence. Review layouts, then approve to compile and render.
        </p>
      )}
    </div>
  );
}
