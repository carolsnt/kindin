"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import SearchBar from "@/components/SearchBar";

export default function HomePage() {
  const router = useRouter();
  const [query, setQuery] = useState("");
  const [author, setAuthor] = useState("");
  const [format, setFormat] = useState("any");
  const [showAuthor, setShowAuthor] = useState(false);

  function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    // TODO: chamar POST /searches e redirecionar para /search/{id}
    router.push("/search/placeholder");
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center px-4 py-16">
      <h1 className="mb-2 text-5xl font-bold tracking-tight">Kindin</h1>
      <p className="mb-10 text-lg text-gray-500 dark:text-gray-400">
        Encontre livros e envie para o seu Kindle.
      </p>

      <form
        onSubmit={handleSearch}
        className="w-full max-w-2xl rounded-2xl border border-gray-200 bg-white p-6 shadow-lg dark:border-gray-700 dark:bg-gray-900"
      >
        <SearchBar
          value={query}
          onChange={setQuery}
          placeholder="Qual livro você quer ler hoje?"
        />

        <button
          type="button"
          onClick={() => setShowAuthor(!showAuthor)}
          className="mt-2 text-sm text-blue-600 hover:underline dark:text-blue-400"
        >
          {showAuthor ? "- Ocultar autor" : "+ Adicionar autor"}
        </button>

        {showAuthor && (
          <input
            type="text"
            value={author}
            onChange={(e) => setAuthor(e.target.value)}
            placeholder="Autor (opcional)"
            className="mt-3 w-full rounded-lg border border-gray-300 px-4 py-3 text-base outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 dark:border-gray-600 dark:bg-gray-800 dark:focus:ring-blue-800"
          />
        )}

        <div className="mt-4 flex items-center gap-3">
          <select
            value={format}
            onChange={(e) => setFormat(e.target.value)}
            className="rounded-lg border border-gray-300 px-4 py-3 text-base outline-none focus:border-blue-500 dark:border-gray-600 dark:bg-gray-800"
          >
            <option value="any">Todos</option>
            <option value="epub">EPUB</option>
            <option value="mobi">MOBI</option>
            <option value="pdf">PDF</option>
          </select>

          <button
            type="submit"
            className="ml-auto rounded-lg bg-blue-600 px-8 py-3 text-base font-semibold text-white hover:bg-blue-700 active:bg-blue-800"
          >
            Buscar
          </button>
        </div>
      </form>
    </main>
  );
}
