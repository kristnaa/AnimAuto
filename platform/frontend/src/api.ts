export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export interface Beat {
  label: string;
  type: string;
  layout: string;
  card_lines?: string[];
  bg_lines?: string[];
  punchline_line?: string;
  code_lines?: string[];
  code_output?: string;
  code_result?: string;
  list_lines?: string[];
}

export interface BeatTypeRegion {
  id: string;
  label: string;
  x: number;
  y: number;
  w: number;
  h: number;
  kind: string;
}

export interface BeatTypeMeta {
  id: string;
  label: string;
  description: string;
  layout: string;
  visuals: string[];
  regions: BeatTypeRegion[];
  script_template: string;
}

export interface Project {
  id: string;
  name: string;
  style_pack: string;
  use_camera: boolean;
  beats: Beat[];
  chat: ChatMessage[];
  code_customized?: boolean;
  updated_at?: string;
}

export interface CodeResponse {
  code: string;
  source: string;
  code_customized: boolean;
}

export interface CodeSaveResponse {
  message: string;
  code_customized: boolean;
  preview_url: string | null;
  render_error: string | null;
}

export interface Snapshot {
  id: string;
  label: string;
  created_at: string;
}

export interface ChatResponse {
  message: string;
  project: Project;
  preview_url: string | null;
  render_error: string | null;
}

const API = "/api";

async function json<T>(url: string, init?: RequestInit): Promise<T> {
  const res = await fetch(url, init);
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    const detail = err.detail;
    const msg = Array.isArray(detail)
      ? detail.map((d: { msg?: string }) => d.msg).join(", ")
      : detail || res.statusText;
    throw new Error(msg);
  }
  return res.json();
}

export async function health() {
  return json<{ status: string; openai_configured: boolean; data_dir: string }>(
    `${API}/health`
  );
}

export async function createProject(name = "Untitled") {
  return json<Project>(`${API}/projects`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  });
}

export async function getProject(id: string) {
  return json<Project>(`${API}/projects/${id}`);
}

export async function sendChat(projectId: string, message: string) {
  return json<ChatResponse>(`${API}/projects/${projectId}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
}

export async function renderProject(
  projectId: string,
  options?: { code?: string; fromBeats?: boolean }
) {
  return json<{ preview_url: string; code_customized?: boolean }>(
    `${API}/projects/${projectId}/render`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        code: options?.code,
        from_beats: options?.fromBeats ?? false,
      }),
    }
  );
}

export async function submitScript(
  projectId: string,
  script: string,
  useAi = false
) {
  return json<ChatResponse>(`${API}/projects/${projectId}/script`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ script, use_ai: useAi }),
  });
}

export async function exportHd(
  projectId: string,
  options?: { code?: string; fromBeats?: boolean }
) {
  return json<{ download_url: string; quality: string }>(
    `${API}/projects/${projectId}/export`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        code: options?.code,
        from_beats: options?.fromBeats ?? false,
      }),
    }
  );
}

export function downloadUrl(projectId: string) {
  return `${API}/projects/${projectId}/download`;
}

export async function getBeatTypes() {
  return json<{ beat_types: BeatTypeMeta[] }>(`${API}/beat-types`);
}

export async function getBeatScriptTemplate() {
  return json<{ filename: string; content: string }>(`${API}/beat-script-template`);
}

export function beatScriptTemplateDownloadUrl() {
  return `${API}/beat-script-template/download`;
}

export async function getProjectCode(projectId: string) {
  return json<CodeResponse>(`${API}/projects/${projectId}/code`);
}

export async function saveProjectCode(
  projectId: string,
  code: string,
  render = true
) {
  return json<CodeSaveResponse>(`${API}/projects/${projectId}/code`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code, render }),
  });
}

export async function regenerateProjectCode(projectId: string) {
  return json<{ code: string; code_customized: boolean; message: string }>(
    `${API}/projects/${projectId}/code/regenerate`,
    { method: "POST" }
  );
}

export async function listSnapshots(projectId: string) {
  return json<Snapshot[]>(`${API}/projects/${projectId}/snapshots`);
}

export async function revertProject(projectId: string, snapshotId: string) {
  return json<{ project: Project; message: string }>(
    `${API}/projects/${projectId}/revert`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ snapshot_id: snapshotId }),
    }
  );
}

export function previewUrl(projectId: string, cacheBust?: number) {
  const q = cacheBust ? `?t=${cacheBust}` : "";
  return `${API}/projects/${projectId}/preview${q}`;
}

export interface PythonDiagnostic {
  line: number;
  column: number;
  end_line: number;
  end_column: number;
  message: string;
  severity: "error" | "warning" | "info";
}

export async function formatPython(code: string) {
  return json<{ code: string }>(`${API}/python/format`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code }),
  });
}

export async function lintPython(code: string) {
  return json<{ diagnostics: PythonDiagnostic[] }>(`${API}/python/lint`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code }),
  });
}
