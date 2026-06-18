import { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState } from "react";
import type { ExcalidrawAnimationUnit, ExcalidrawPageUnits } from "../api";
import { excalidrawPagePreviewUrl } from "../api";

interface ExcalidrawPagePreviewProps {
  projectId: string;
  page: ExcalidrawPageUnits;
  orderedUnits: ExcalidrawAnimationUnit[];
  selectedUnitIndex: number | null;
  hoveredUnitIndex: number | null;
  onSelectUnit: (unitIndex: number) => void;
  onHoverUnit: (unitIndex: number | null) => void;
  disabled?: boolean;
  /** Full-size canvas in the main preview panel (vs compact sidebar strip). */
  variant?: "compact" | "canvas";
  /** Bust browser cache when the uploaded drawing changes. */
  cacheKey?: string | number;
}

interface ContentBox {
  left: number;
  top: number;
  width: number;
  height: number;
}

interface NormalizedBBox {
  x: number;
  y: number;
  width: number;
  height: number;
}

function normalizeBBox(unit: ExcalidrawAnimationUnit): NormalizedBBox | null {
  const raw = unit.bbox;
  if (!raw) return null;
  if (Array.isArray(raw)) {
    const [x, y, width, height] = raw;
    return { x, y, width, height };
  }
  return raw;
}

function mapBBoxToOverlay(
  bbox: NormalizedBBox,
  content: ContentBox,
  pageWidth: number,
  pageHeight: number
) {
  const scaleX = content.width / pageWidth;
  const scaleY = content.height / pageHeight;
  return {
    left: content.left + bbox.x * scaleX,
    top: content.top + bbox.y * scaleY,
    width: bbox.width * scaleX,
    height: bbox.height * scaleY,
  };
}

export function ExcalidrawPagePreview({
  projectId,
  page,
  orderedUnits,
  selectedUnitIndex,
  hoveredUnitIndex,
  onSelectUnit,
  onHoverUnit,
  disabled,
  variant = "compact",
  cacheKey,
}: ExcalidrawPagePreviewProps) {
  const pageWidth = page.page_width || 854;
  const pageHeight = page.page_height || 480;
  const previewUrl = excalidrawPagePreviewUrl(projectId, page.page_index, cacheKey);
  const stageRef = useRef<HTMLDivElement>(null);
  const imgRef = useRef<HTMLImageElement>(null);
  const hitRefs = useRef<Map<number, HTMLButtonElement>>(new Map());
  const [contentBox, setContentBox] = useState<ContentBox | null>(null);

  const stepByUnitIndex = useMemo(() => {
    const map = new Map<number, number>();
    orderedUnits.forEach((unit, step) => map.set(unit.index, step + 1));
    return map;
  }, [orderedUnits]);

  const hitTargets = useMemo(() => {
    return page.units
      .map((unit) => {
        const bbox = normalizeBBox(unit);
        if (!bbox || bbox.width <= 0 || bbox.height <= 0) return null;
        return {
          unit,
          bbox,
          step: stepByUnitIndex.get(unit.index) ?? null,
        };
      })
      .filter((item): item is NonNullable<typeof item> => item !== null)
      .sort((a, b) => a.bbox.width * a.bbox.height - b.bbox.width * b.bbox.height);
  }, [page.units, stepByUnitIndex]);

  const measureContentBox = useCallback(() => {
    const stage = stageRef.current;
    const img = imgRef.current;
    if (!stage || !img) return;
    const stageRect = stage.getBoundingClientRect();
    const imgRect = img.getBoundingClientRect();
    if (imgRect.width <= 0 || imgRect.height <= 0) return;
    setContentBox({
      left: imgRect.left - stageRect.left + stage.scrollLeft,
      top: imgRect.top - stageRect.top + stage.scrollTop,
      width: imgRect.width,
      height: imgRect.height,
    });
  }, []);

  useLayoutEffect(() => {
    measureContentBox();
  }, [measureContentBox, previewUrl, page.page_index, variant]);

  useEffect(() => {
    const stage = stageRef.current;
    if (!stage || typeof ResizeObserver === "undefined") return;
    const observer = new ResizeObserver(() => measureContentBox());
    observer.observe(stage);
    if (imgRef.current) observer.observe(imgRef.current);
    return () => observer.disconnect();
  }, [measureContentBox]);

  useEffect(() => {
    if (selectedUnitIndex == null) return;
    const node = hitRefs.current.get(selectedUnitIndex);
    node?.scrollIntoView({ block: "nearest", inline: "nearest", behavior: "smooth" });
  }, [selectedUnitIndex, contentBox]);

  const isCanvas = variant === "canvas";

  return (
    <div className={`excal-sequence-preview ${isCanvas ? "excal-sequence-preview-canvas" : ""}`}>
      {!isCanvas && (
        <div className="excal-sequence-preview-header">
          <span>Page preview</span>
          <span className="excal-sequence-preview-hint">Click an element to select it in the list</span>
        </div>
      )}
      <div
        ref={stageRef}
        className={`excal-sequence-preview-stage ${isCanvas ? "canvas" : ""}`}
        style={isCanvas ? undefined : { aspectRatio: `${pageWidth} / ${pageHeight}` }}
      >
        <img
          ref={imgRef}
          className="excal-sequence-preview-image"
          src={previewUrl}
          alt={page.page_name}
          draggable={false}
          onLoad={measureContentBox}
        />
        {contentBox && (
          <div className="excal-sequence-preview-overlay">
            {hitTargets.map(({ unit, bbox, step }) => {
              const box = mapBBoxToOverlay(bbox, contentBox, pageWidth, pageHeight);
              const isSelected = selectedUnitIndex === unit.index;
              const isHovered = hoveredUnitIndex === unit.index;
              return (
                <button
                  key={unit.unit_id}
                  ref={(node) => {
                    if (node) hitRefs.current.set(unit.index, node);
                    else hitRefs.current.delete(unit.index);
                  }}
                  type="button"
                  className={[
                    "excal-sequence-hit",
                    `kind-${unit.kind}`,
                    isSelected ? "selected" : "",
                    isHovered ? "hovered" : "",
                  ]
                    .filter(Boolean)
                    .join(" ")}
                  style={{
                    left: `${box.left}px`,
                    top: `${box.top}px`,
                    width: `${Math.max(box.width, 6)}px`,
                    height: `${Math.max(box.height, 6)}px`,
                  }}
                  title={unit.label}
                  disabled={disabled}
                  onClick={() => onSelectUnit(unit.index)}
                  onMouseEnter={() => onHoverUnit(unit.index)}
                  onMouseLeave={() => onHoverUnit(null)}
                >
                  {step != null && (isSelected || isHovered) && (
                    <span className="excal-sequence-hit-step" aria-hidden="true">
                      {step}
                    </span>
                  )}
                </button>
              );
            })}
          </div>
        )}
      </div>
      {isCanvas && (
        <div className="excal-sequence-preview-footer">
          <span>{page.page_name}</span>
          <span className="excal-sequence-preview-hint">
            Click an element to highlight it in the draw-order list
          </span>
        </div>
      )}
    </div>
  );
}
