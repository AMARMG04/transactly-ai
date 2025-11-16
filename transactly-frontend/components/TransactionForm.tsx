"use client";

import { useState } from "react";

interface Props {
  loading: boolean;
  onSubmit: (text: string) => void;
}

export default function TransactionForm({ loading, onSubmit }: Props) {
  const [text, setText] = useState("");

  return (
    <div className="card">
      <div className="section-title">Input</div>
      <p className="section-desc">
        Paste a transaction statement and classify it.
      </p>

      <label className="input-label">Transaction statement</label>
      <textarea
        className="w-full mt-2 border border-border p-3 text-sm focus:outline-none focus:ring-2 focus:ring-accent"
        placeholder='e.g. "ZOMATO PAYMENT 450 INR"'
        rows={4}
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <div className="flex items-center gap-3 mt-4">
        <button
          className="render-btn"
          disabled={loading || !text.trim()}
          onClick={() => onSubmit(text)}
        >
          {loading ? "Classifying…" : "Classify"}
        </button>

        <button className="render-btn-ghost" onClick={() => setText("")}>
          Clear
        </button>
      </div>
    </div>
  );
}