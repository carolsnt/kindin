import ResultItem from "./ResultItem";

interface Result {
  result_id: string;
  filename: string;
  format: string;
  file_size?: number;
  title_raw?: string;
  author_raw?: string;
}

interface ResultListProps {
  results: Result[];
}

export default function ResultList({ results }: ResultListProps) {
  if (results.length === 0) return null;

  return (
    <ul className="space-y-3">
      {results.map((r) => (
        <ResultItem key={r.result_id} result={r} />
      ))}
    </ul>
  );
}
