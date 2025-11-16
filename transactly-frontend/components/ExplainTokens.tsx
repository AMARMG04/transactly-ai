"use client";

import { ExplanationToken } from "../types";

export default function ExplainTokens({
  text,
  explanation,
}: {
  text: string;
  explanation: ExplanationToken[];
}) {
  if (!text) return null;

  const map: Record<string, number> = {};
  explanation.forEach((e) => (map[e.token.toLowerCase()] = e.importance));

  return (
    <p className="text-sm leading-6 mt-2">
      {text.split(" ").map((word, i) => {
        const key = word.toLowerCase().replace(/[^\w]/g, "");
        const score = map[key];

        if (score !== undefined) {
          return (
            <span
              key={i}
              className="underline decoration-accent decoration-2 underline-offset-4 mr-1 font-medium"
            >
              {word}
            </span>
          );
        }

        return <span key={i} className="mr-1 text-muted">{word}</span>;
      })}
    </p>
  );
}