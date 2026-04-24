"use client";

import { useEffect, useState } from "react";
import ResultList from "@/components/ResultList";
import { connectSSE } from "@/lib/sse";

interface Result {
  result_id: string;
  filename: string;
  format: string;
  file_size?: number;
  title_raw?: string;
  author_raw?: string;
}

export default function SearchPage({ params }: { params: { id: string } }) {
  const [results, setResults] = useState<Result[]>([]);
  const [status, setStatus] = useState<"running" | "done" | "error">("running");

  useEffect(() => {
    if (params.id === "placeholder") {
      setStatus("done");
      return;
    }

    const close = connectSSE(
      `/searches/${params.id}/events`,
      {
        result: (data: unknown) => setResults((prev) => [...prev, data as Result]),
        done: () => setStatus("done"),
        error: () => setStatus("error"),
      }
    );

    return close;
  }, [params.id]);

  return (
    <main className="mx-auto max-w-4xl px-4 py-10">
      <h1 className="mb-6 text-2xl font-bold">
        Resultados {status === "running" && <span className="text-sm font-normal text-blue-500">buscando…</span>}
      </h1>
      <ResultList results={results} />
      {status === "done" && results.length === 0 && (
        <p className="text-gray-500">Nenhum resultado encontrado.</p>
      )}
    </main>
  );
}
