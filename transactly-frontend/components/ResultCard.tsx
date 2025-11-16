"use client";

import { useState } from "react";
import Skeleton from "./Skeleton";
import { ClassificationResult } from "../types";
import ConfidenceBar from "./ConfidenceBar";
import ExplainTokens from "./ExplainTokens";

const CATEGORY_OPTIONS = [
  "Food & Dining",
  "Shopping",
  "Fuel",
  "Travel & Transport",
  "Utilities",
  "Health & Fitness",
  "Entertainment",
  "Bills & Subscriptions",
  "Groceries",
  "Others"
];

export default function ResultCard({ result, loading }: { result: ClassificationResult | null; loading: boolean }) {
  const [corrected, setCorrected] = useState("");
  const [status, setStatus] = useState<"idle" | "sending" | "success" | "error">("idle");

  if (loading) {
    return (
      <div className="card space-y-4">
        <Skeleton height={24} />
        <Skeleton height={22} />
        <Skeleton height={100} />
      </div>
    );
  }

  if (!result) return null;

  if (result.error)
    return (
      <div className="card">
        <h2 className="text-lg font-semibold">Error</h2>
        <p className="text-muted text-sm mt-1">{result.message}</p>
      </div>
    );

  const pct = Math.round((result.confidence || 0) * 100);

  const submitFeedback = async () => {
    if (!corrected || corrected === result.category) return;
    setStatus("sending");

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/feedback/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          description: result.original_text,
          predicted_category: result.category,
          corrected_category: corrected,
          method: result.method ?? "model",
          confidence: result.confidence
        }),
      });

      if (res.ok) {
        setStatus("success");
        setCorrected("");
      } else {
        setStatus("error");
      }
    } catch {
      setStatus("error");
    }
  };

  let confidenceLabel = "";
  let confidenceColor = "";

  if (pct >= 75) {
    confidenceLabel = "High Confidence";
    confidenceColor = "bg-green-100 text-green-800";
  } else if (pct >= 55) {
    confidenceLabel = "Medium Confidence";
    confidenceColor = "bg-purple-100 text-purple-800";
  } else {
    confidenceLabel = "Low Confidence";
    confidenceColor = "bg-red-100 text-red-800";
  }

  return (
    <div className="card space-y-8">

      {/* Prediction Summary */}
      <section>
        <div className="flex items-center gap-2 mb-1">
          <span className="text-xl">🧠</span>
          <h2 className="text-lg font-semibold">Prediction</h2>
        </div>

        <div className="mt-1">
          <p className="text-2xl font-semibold text-[#7c5cff]">{result.category}</p>

          <div className={`mt-2 inline-block px-3 py-1 rounded-full text-xs font-medium ${confidenceColor}`}>
            {confidenceLabel}
          </div>
        </div>

        <div className="mt-4">
          <p className="text-muted text-sm mb-1">Confidence</p>
          <ConfidenceBar value={result.confidence} />
        </div>

        <div className="mt-3">
          <span className="font-medium">Method </span><br /> <span className="badge">{result.method ?? "model"}</span>
        </div>
      </section>

      {/* <hr className="border border-gray-100" /> */}

      {/* Explanation */}
      {/* <section>
        <div className="flex items-center gap-2 mb-1">
          <span className="text-xl">🔍</span>
          <h3 className="text-lg font-semibold">Why</h3>
        </div>

        <p className="text-muted text-sm mb-2">
          Key parts of the text influencing the prediction.
        </p>

        <ExplainTokens text={result.original_text} explanation={result.explanation} />
      </section> */}

      {/* <hr className="border border-gray-100" /> */}

      {/* Feedback */}
      <section>
        <div className="flex items-center gap-2 mb-1">
          <span className="text-xl">📝</span>
          <h3 className="text-lg font-semibold">Was this correct?</h3>
        </div>

        <p className="text-muted text-sm mb-2">
          Help us improve by selecting the correct category.
        </p>

        <select
          title="category"
          value={corrected}
          onChange={(e) => setCorrected(e.target.value)}
          className="w-full p-2 border border-border rounded-md text-sm"
        >
          <option value="">Select correct category</option>
          {CATEGORY_OPTIONS.map((c) => (
            <option key={c}>{c}</option>
          ))}
        </select>

        <button
          onClick={submitFeedback}
          disabled={!corrected || corrected === result.category}
          className="mt-3 render-btn disabled:opacity-50"
        >
          {status === "sending" ? "Submitting…" : "Submit Feedback"}
        </button>

        {status === "success" && (
          <p className="text-green-600 text-sm mt-1">Feedback saved. Thank you! 🎉</p>
        )}
        {status === "error" && (
          <p className="text-red-600 text-sm mt-1">Failed to send feedback.</p>
        )}
      </section>
    </div>
  );
}