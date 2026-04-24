interface ActionsBarProps {
  resultId: string;
}

export default function ActionsBar({ resultId }: ActionsBarProps) {
  return (
    <div className="flex flex-col gap-2 text-sm">
      <button
        className="rounded bg-blue-600 px-3 py-1 text-white hover:bg-blue-700"
        onClick={() => alert(`Enviar ${resultId} (em breve)`)}
      >
        Enviar
      </button>
      <button
        className="rounded border border-gray-300 px-3 py-1 hover:bg-gray-50 dark:border-gray-600 dark:hover:bg-gray-800"
        onClick={() => alert(`Compartilhar ${resultId} (em breve)`)}
      >
        Compartilhar
      </button>
      <button
        className="rounded border border-gray-300 px-3 py-1 hover:bg-gray-50 dark:border-gray-600 dark:hover:bg-gray-800"
        onClick={() => alert(`Baixar ${resultId} (em breve)`)}
      >
        Baixar
      </button>
    </div>
  );
}
