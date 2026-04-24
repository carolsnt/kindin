"use client";

import { useState } from "react";
import ActionsBar from "./ActionsBar";

interface Result {
  result_id: string;
  filename: string;
  format: string;
  file_size?: number;
  title_raw?: string;
  author_raw?: string;
}

interface ResultItemProps {
  result: Result;
}

export default function ResultItem({ result }: ResultItemProps) {
  const [selected, setSelected] = useState(false);

  return (
    <li className="flex items-start gap-3 rounded-lg border border-gray-200 p-4 dark:border-gray-700">
      <input
        type="checkbox"
        checked={selected}
        onChange={(e) => setSelected(e.target.checked)}
        className="mt-1 h-4 w-4 accent-blue-600"
      />
      <div className="flex-1">
        <p className="font-medium">{result.title_raw ?? result.filename}</p>
        {result.author_raw && (
          <p className="text-sm text-gray-500">{result.author_raw}</p>
        )}
        <div className="mt-1 flex gap-2 text-xs text-gray-400">
          <span className="rounded bg-gray-100 px-2 py-0.5 dark:bg-gray-800">
            {result.format.toUpperCase()}
          </span>
          {result.file_size && (
            <span>{(result.file_size / 1024 / 1024).toFixed(1)} MB</span>
          )}
        </div>
      </div>
      {selected && <ActionsBar resultId={result.result_id} />}
    </li>
  );
}
