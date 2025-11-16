// types.ts

export interface ExplanationToken {
  token: string;
  importance: number;
}

export interface CategoryScores {
  [category: string]: number;
}

export interface ExplanationToken {
  token: string;
  importance: number;
}


export interface ClassificationResult {
  category: string;                     // final predicted category
  confidence: number;                   // 0–1 float
  original_text: string;                // user's input text
  explanation: ExplanationToken[];      // token-level importance
  category_scores: CategoryScores;      // for confidence bar comparisons

  method?: string;                      // "rule", "model", "hybrid", etc.

  similar_examples?: string[];          // optional example list

  error?: boolean;                      // error flag
  message?: string;                     // error message
}

export interface FeedbackPayload {
  description: string;
  predicted_category: string;
  corrected_category: string;
  method: string;
  confidence: number;
}