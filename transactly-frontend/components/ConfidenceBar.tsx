"use client";

export default function ConfidenceBar({ value }: { value: number }) {
  const pct = Math.round((value || 0) * 100);

  return (
    <div className="mt-2">
      <div className="h-2 w-full bg-gray-200 rounded-full overflow-hidden">
        <div
          className="h-full bg-accent transition-all duration-300"
          style={{ width: `${pct}%` }}
        />
      </div>
      <p className="text-sm text-muted mt-1">{pct}%</p>
    </div>
  );
}