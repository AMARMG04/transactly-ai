"use client";

import { useState } from "react";
import TransactionForm from "../components/TransactionForm";
import ResultCard from "../components/ResultCard";
import { ClassificationResult } from "../types";

export default function Page() {
  const [result, setResult] = useState<ClassificationResult | null>(null);
  const [loading, setLoading] = useState(false);

  const classify = async (text: string) => {
    setLoading(true);
    setResult(null);

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/classify`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setResult({
        category: "Error",
        confidence: 0,
        original_text: "",
        explanation: [],
        category_scores: {},
        error: true,
        message: "Failed to reach backend",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <TransactionForm loading={loading} onSubmit={classify} />

      {result && <ResultCard result={result} loading={loading} />}
    </>
  );
}