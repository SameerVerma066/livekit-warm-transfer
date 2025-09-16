// frontend/components/Logs.tsx
interface LogsProps {
  logs: string[];
}

export default function Logs({ logs }: LogsProps) {
  return (
    <pre className="p-4 border rounded bg-gray-900 text-green-300 font-mono text-sm h-48 overflow-y-auto whitespace-pre-wrap">
      {logs.length > 0 ? logs.join('\n') : 'Logs will appear here...'}
    </pre>
  );
}
