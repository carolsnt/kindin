"use client";

export default function DestinationsPage() {
  return (
    <main className="mx-auto max-w-3xl px-4 py-10">
      <h1 className="mb-6 text-2xl font-bold">Meus Destinos</h1>
      <table className="w-full rounded-lg border border-gray-200 text-sm dark:border-gray-700">
        <thead>
          <tr className="bg-gray-50 dark:bg-gray-800">
            <th className="px-4 py-3 text-left">Label</th>
            <th className="px-4 py-3 text-left">Tipo</th>
            <th className="px-4 py-3 text-left">Valor</th>
            <th className="px-4 py-3 text-left">Default</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td colSpan={4} className="px-4 py-6 text-center text-gray-400">
              Nenhum destino cadastrado.
            </td>
          </tr>
        </tbody>
      </table>
      {/* TODO: integrar com GET/POST /me/destinations */}
    </main>
  );
}
