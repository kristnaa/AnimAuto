import { useCallback, useEffect, useRef } from "react";
import Editor, { Monaco, OnMount } from "@monaco-editor/react";
import type { editor as MonacoEditor } from "monaco-editor";

export interface CodeDiagnostic {
  line: number;
  column: number;
  end_line: number;
  end_column: number;
  message: string;
  severity: "error" | "warning" | "info";
}

interface CodeEditorProps {
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
  onFormat?: (code: string) => Promise<string>;
  onLint?: (code: string) => Promise<CodeDiagnostic[]>;
}

export function CodeEditor({
  value,
  onChange,
  disabled = false,
  onFormat,
  onLint,
}: CodeEditorProps) {
  const editorRef = useRef<MonacoEditor.IStandaloneCodeEditor | null>(null);
  const monacoRef = useRef<Monaco | null>(null);
  const lintTimerRef = useRef<number | null>(null);

  const applyDiagnostics = useCallback(
    (diagnostics: CodeDiagnostic[]) => {
      const editor = editorRef.current;
      const monaco = monacoRef.current;
      if (!editor || !monaco) return;

      const model = editor.getModel();
      if (!model) return;

      monaco.editor.setModelMarkers(
        model,
        "manimations-lint",
        diagnostics.map((d) => ({
          startLineNumber: d.line,
          startColumn: d.column,
          endLineNumber: d.end_line,
          endColumn: d.end_column,
          message: d.message,
          severity:
            d.severity === "error"
              ? monaco.MarkerSeverity.Error
              : d.severity === "warning"
                ? monaco.MarkerSeverity.Warning
                : monaco.MarkerSeverity.Info,
        })),
      );
    },
    [],
  );

  const runLint = useCallback(
    async (code: string) => {
      if (!onLint) return;
      try {
        const diagnostics = await onLint(code);
        applyDiagnostics(diagnostics);
      } catch {
        /* ignore lint failures */
      }
    },
    [applyDiagnostics, onLint],
  );

  const scheduleLint = useCallback(
    (code: string) => {
      if (!onLint) return;
      if (lintTimerRef.current) {
        window.clearTimeout(lintTimerRef.current);
      }
      lintTimerRef.current = window.setTimeout(() => {
        void runLint(code);
      }, 450);
    },
    [onLint, runLint],
  );

  const handleMount: OnMount = (editor, monaco) => {
    editorRef.current = editor;
    monacoRef.current = monaco;

    editor.updateOptions({
      readOnly: disabled,
      minimap: { enabled: true },
      fontSize: 13,
      lineHeight: 20,
      fontFamily: '"JetBrains Mono", "SF Mono", Menlo, monospace',
      scrollBeyondLastLine: false,
      wordWrap: "off",
      tabSize: 4,
      insertSpaces: true,
      automaticLayout: true,
      padding: { top: 12, bottom: 12 },
      renderWhitespace: "selection",
      bracketPairColorization: { enabled: true },
      smoothScrolling: true,
    });

    editor.addAction({
      id: "format-python",
      label: "Format Document",
      keybindings: [monaco.KeyMod.CtrlCmd | monaco.KeyMod.Shift | monaco.KeyCode.KeyF],
      run: async () => {
        if (!onFormat) return;
        const current = editor.getValue();
        try {
          const formatted = await onFormat(current);
          onChange(formatted);
          editor.setValue(formatted);
          void runLint(formatted);
        } catch {
          /* keep current code */
        }
      },
    });

    void runLint(value);
  };

  useEffect(() => {
    editorRef.current?.updateOptions({ readOnly: disabled });
  }, [disabled]);

  useEffect(() => {
    scheduleLint(value);
  }, [value, scheduleLint]);

  useEffect(
    () => () => {
      if (lintTimerRef.current) {
        window.clearTimeout(lintTimerRef.current);
      }
    },
    [],
  );

  return (
    <div className="monaco-code-editor">
      <Editor
        height="100%"
        language="python"
        theme="vs-dark"
        value={value}
        onChange={(next) => onChange(next ?? "")}
        onMount={handleMount}
        options={{
          readOnly: disabled,
        }}
      />
    </div>
  );
}
