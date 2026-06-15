import { useRef, useState } from "react";
import { Loader2, Mic, Paperclip } from "lucide-react";
import type { Project, VoiceMotionData } from "../api";
import { uploadVoiceAudio } from "../api";

interface VoiceMotionPanelProps {
  projectId: string;
  voiceMotion: VoiceMotionData | null | undefined;
  enabled: boolean;
  onToggle: (enabled: boolean) => void;
  onUploaded: (voice: VoiceMotionData) => void;
  disabled?: boolean;
}

function formatTime(sec: number): string {
  const m = Math.floor(sec / 60);
  const s = Math.floor(sec % 60);
  return `${m}:${s.toString().padStart(2, "0")}`;
}

export function VoiceMotionPanel({
  projectId,
  voiceMotion,
  enabled,
  onToggle,
  onUploaded,
  disabled,
}: VoiceMotionPanelProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFile = async (file: File) => {
    setUploading(true);
    setError(null);
    try {
      const res = await uploadVoiceAudio(projectId, file);
      onUploaded(res.voice_motion);
      onToggle(true);
    } catch (e) {
      setError(String(e));
    } finally {
      setUploading(false);
      if (inputRef.current) inputRef.current.value = "";
    }
  };

  return (
    <div className="voiceover-panel">
      <div className="voice-motion-toolbar">
        <button
          type="button"
          className={`voice-motion-toggle ${enabled ? "active" : ""}`}
          onClick={() => onToggle(!enabled)}
          disabled={disabled}
          title="Voice motion mode — black canvas, shapes, no cards/icons"
        >
          <Mic size={14} />
          Voice motion
        </button>
        <button
          type="button"
          className="btn-ghost sm"
          onClick={() => inputRef.current?.click()}
          disabled={disabled || uploading}
          title="Upload narration (MP3, WAV, M4A)"
        >
          {uploading ? <Loader2 size={14} className="spin" /> : <Paperclip size={14} />}
          Upload audio
        </button>
        <input
          ref={inputRef}
          type="file"
          accept="audio/*,.mp3,.wav,.m4a,.webm,.ogg,.flac,.aac"
          hidden
          onChange={(e) => {
            const file = e.target.files?.[0];
            if (file) handleFile(file);
          }}
        />
        {voiceMotion?.audio_filename && (
          <span className="voice-motion-chip">
            {voiceMotion.audio_filename}
            {voiceMotion.duration_sec != null && (
              <span className="voice-motion-chip-meta">{formatTime(voiceMotion.duration_sec)}</span>
            )}
          </span>
        )}
      </div>
      {enabled && (
        <p className="voiceover-hint">
          Upload narration, generate a <strong>storyboard</strong> (one page per sentence), review
          layouts, then approve to compile Manim code and render with your voice muxed in.
        </p>
      )}
      {error && <div className="error-bar compact">{error}</div>}
      {enabled && voiceMotion?.segments && voiceMotion.segments.length > 0 && (
        <ol className="voice-segment-list">
          {voiceMotion.segments.map((seg, i) => (
            <li key={i}>
              <span className="voice-segment-time">
                {formatTime(seg.start)}–{formatTime(seg.end)}
              </span>
              <span className="voice-segment-text">{seg.text}</span>
            </li>
          ))}
        </ol>
      )}
    </div>
  );
}

export function isVoiceMotionProject(project: Project | null | undefined): boolean {
  return project?.creation_mode === "voice_motion";
}
