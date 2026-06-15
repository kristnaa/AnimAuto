import { useRef, useState } from "react";
import { BeatStatement, StatementMode, projectMediaUrl, uploadProjectMedia } from "../api";
import { Button } from "./Button";

const MODES: { value: StatementMode; label: string; hint: string }[] = [
  { value: "auto", label: "Auto (from content)", hint: "Detect from text / image / video filled in" },
  { value: "text", label: "Text only", hint: "Typed lines inside the card" },
  { value: "image", label: "Image only", hint: "Single image fills the card" },
  { value: "video", label: "Video only", hint: "Looping video clip inside the card" },
  { value: "text_image", label: "Text + image", hint: "Lines on top, image below" },
  { value: "text_video", label: "Text + video", hint: "Lines on top, video below" },
  { value: "text_image_video", label: "Text + image + video", hint: "All three stacked" },
];

function modeUsesText(mode: StatementMode): boolean {
  return mode === "auto" || mode.includes("text");
}

function modeUsesImage(mode: StatementMode): boolean {
  return mode === "auto" || mode.includes("image");
}

function modeUsesVideo(mode: StatementMode): boolean {
  return mode === "auto" || mode.includes("video");
}

interface StatementBeatPanelProps {
  projectId: string;
  statement: BeatStatement;
  onChange: (next: BeatStatement) => void;
  /** When nested inside the Content tab, omit the panel intro blurb. */
  embedded?: boolean;
}

export function StatementBeatPanel({
  projectId,
  statement,
  onChange,
  embedded = false,
}: StatementBeatPanelProps) {
  const [uploading, setUploading] = useState<"image" | "video" | null>(null);
  const [error, setError] = useState<string | null>(null);
  const imageInputRef = useRef<HTMLInputElement>(null);
  const videoInputRef = useRef<HTMLInputElement>(null);

  const mode = (statement.mode || "auto") as StatementMode;
  const text = (statement.text_lines || []).join("\n");

  const patch = (partial: Partial<BeatStatement>) => {
    onChange({ ...statement, ...partial });
  };

  const handleUpload = async (slot: "image" | "video", file: File) => {
    setUploading(slot);
    setError(null);
    try {
      const res = await uploadProjectMedia(projectId, file);
      if (slot === "image") {
        patch({ image: { ref: res.ref, kind: res.kind } });
      } else {
        patch({ video: { ref: res.ref, kind: res.kind, loop: true, muted: true } });
      }
    } catch (e) {
      setError(String(e));
    } finally {
      setUploading(null);
    }
  };

  return (
    <div className="statement-beat-panel">
      {!embedded && (
        <p className="statement-beat-intro">
          One full-width card below the label. Choose what goes inside — text, image, video, or any
          combination.
        </p>
      )}

      <label className="beat-field">
        <span>Card content mode</span>
        <select
          value={mode}
          onChange={(e) => patch({ mode: e.target.value as StatementMode })}
        >
          {MODES.map((m) => (
            <option key={m.value} value={m.value}>
              {m.label}
            </option>
          ))}
        </select>
        <small className="field-hint">{MODES.find((m) => m.value === mode)?.hint}</small>
      </label>

      {modeUsesText(mode) && (
        <label className="beat-field">
          <span>Card text (one line per row)</span>
          <textarea
            rows={5}
            value={text}
            placeholder="First line&#10;Second line"
            onChange={(e) =>
              patch({
                text_lines: e.target.value.split("\n").filter((l) => l.trim()),
              })
            }
          />
        </label>
      )}

      {modeUsesImage(mode) && (
        <div className="statement-media-block">
          <div className="statement-media-header">
            <span className="statement-media-label">Image</span>
            <div className="statement-media-actions">
              <input
                ref={imageInputRef}
                type="file"
                accept="image/png,image/jpeg,image/webp,image/gif,image/svg+xml"
                hidden
                onChange={(e) => {
                  const file = e.target.files?.[0];
                  if (file) handleUpload("image", file);
                  e.target.value = "";
                }}
              />
              <Button
                type="button"
                variant="primary"
                disabled={uploading === "image"}
                onClick={() => imageInputRef.current?.click()}
              >
                {uploading === "image" ? "Uploading…" : "Upload image"}
              </Button>
              {statement.image?.ref && (
                <Button type="button" variant="ghost" onClick={() => patch({ image: undefined })}>
                  Remove
                </Button>
              )}
            </div>
          </div>
          {statement.image?.ref ? (
            <div className="statement-media-preview">
              <img src={projectMediaUrl(projectId, statement.image.ref)} alt="Statement" />
              <code>{statement.image.ref}</code>
            </div>
          ) : (
            <p className="statement-media-empty">No image — upload PNG, JPG, WEBP, GIF, or SVG.</p>
          )}
        </div>
      )}

      {modeUsesVideo(mode) && (
        <div className="statement-media-block">
          <div className="statement-media-header">
            <span className="statement-media-label">Video</span>
            <div className="statement-media-actions">
              <input
                ref={videoInputRef}
                type="file"
                accept="video/mp4,video/webm,video/quicktime"
                hidden
                onChange={(e) => {
                  const file = e.target.files?.[0];
                  if (file) handleUpload("video", file);
                  e.target.value = "";
                }}
              />
              <Button
                type="button"
                variant="primary"
                disabled={uploading === "video"}
                onClick={() => videoInputRef.current?.click()}
              >
                {uploading === "video" ? "Uploading…" : "Upload video"}
              </Button>
              {statement.video?.ref && (
                <Button type="button" variant="ghost" onClick={() => patch({ video: undefined })}>
                  Remove
                </Button>
              )}
            </div>
          </div>
          {statement.video?.ref ? (
            <div className="statement-media-preview video">
              <video
                src={projectMediaUrl(projectId, statement.video.ref)}
                controls
                muted
                loop
                playsInline
              />
              <code>{statement.video.ref}</code>
            </div>
          ) : (
            <p className="statement-media-empty">No video — upload MP4, WEBM, or MOV (max 25 MB).</p>
          )}
        </div>
      )}

      {error && <p className="form-error">{error}</p>}
    </div>
  );
}
