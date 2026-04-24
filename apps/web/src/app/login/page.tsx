export default function LoginPage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center px-4">
      <h1 className="mb-6 text-3xl font-bold">Entrar no Kindin</h1>
      <p className="mb-8 text-gray-500">
        Faça login com o Telegram para acessar todas as funcionalidades.
      </p>
      {/* TODO: integrar Telegram Login Widget */}
      <div className="rounded-lg border border-dashed border-gray-300 px-8 py-6 text-center text-gray-400">
        Telegram Login Widget (em breve)
      </div>
    </main>
  );
}
