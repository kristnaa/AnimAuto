import { useRef, useState } from "react";
import { Loader2, PenLine, Paperclip, Play } from "lucide-react";
import type { Project } from "../api";
import { generateExcalidrawAnimation, uploadExcalidrawDrawing } from "../api";

interface ExcalidrawPanelProps {
  project: Project;
  onUpdated: (project: Project, code?: string) => void;
  onRender: () => void;
  disabled?: boolean;
  rendering?: boolean;
}

export function ExcalidrawPanel({
  project,
  onUpdated,
  onRender,
  disabled,
  rendering,
}: ExcalidrawPanelProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [uploading, setUploading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const excalidraw = project.excalidraw;

  const handleUpload = async (file: File) => {
    setUploading(true);
    setError(null);
    try {
      const res = await uploadExcalidrawDrawing(project.id, file);
      onUpdated({
        ...project,
        creation_mode: "excalidraw",
        excalidraw: res.excalidraw,
        code_customized: true,
      });
    } catch (e) {
      setError(String(e));
    } finally {
      setUploading(false);
      if (inputRef.current) inputRef.current.value = "";
    }
  };

  const handleGenerate = async () => {
    setGenerating(true);
    setError(null);
    try {
      const res = await generateExcalidrawAnimation(project.id);
      onUpdated(res.project, res.code);
    } catch (e) {
      setError(String(e));
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="voiceover-panel">
      <div className="voice-motion-toolbar">
        <span className="voice-motion-toggle active" title="Excalidraw sketch animation">
          <PenLine size={14} />
          Excalidraw
        </span>
        <button
          type="button"
          className="btn-ghost sm"
          onClick={() => inputRef.current?.click()}
          disabled={disabled || uploading}
          title="Upload Excalidraw .svg export or .excalidraw file"
        >
          {uploading ? <Loader2 size={14} className="spin" /> : <Paperclip size={14} />}
          Upload drawing
        </button>
        <input
          ref={inputRef}
          type="file"
          accept=".svg,.excalidraw,image/svg+xml,application/json"
          hidden
          onChange={(e) => {
            const file = e.target.files?.[0];
            if (file) void handleUpload(file);
          }}
        />
        {excalidraw?.drawing_filename && (
          <span className="voice-motion-chip">{excalidraw.drawing_filename}</span>
        )}
        <button
          type="button"
          className="btn-primary sm"
          onClick={() => void handleGenerate()}
          disabled={disabled || generating || !excalidraw?.drawing_ref}
          title="Compile Manim scene from uploaded drawing"
        >
          {generating ? <Loader2 size={14} className="spin" /> : <Play size={14} />}
          Generate animation
        </button>
        <button
          type="button"
          className="btn-ghost sm"
          onClick={onRender}
          disabled={disabled || rendering || !excalidraw?.drawing_ref}
          title="Render preview video"
        >
          {rendering ? <Loader2 size={14} className="spin" /> : "Render"}
        </button>
      </div>
      <p className="voiceover-hint">
        Draw in <strong>Excalidraw</strong>, export as <strong>.svg</strong> (or save{" "}
        <strong>.excalidraw</strong>), upload here, then <strong>Generate animation</strong> and{" "}
        <strong>Render</strong>. Multiple frames/pages animate one full screen at a time. Use chat for
        draw order within each page.
      </p>
      {error && <div className="error-bar compact">{error}</div>}
    </div>
  );
}

export function isExcalidrawProject(project: Project | null | undefined): boolean {
  return project?.creation_mode === "excalidraw" || Boolean(project?.excalidraw?.drawing_ref);
}
