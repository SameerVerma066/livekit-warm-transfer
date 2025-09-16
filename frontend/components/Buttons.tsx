// frontend/components/Button.tsx
import React, { ReactNode } from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
}

export default function Button({ children, ...props }: ButtonProps) {
  return (
    <button
      className="py-2 px-4 font-semibold rounded bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50"
      {...props}
    >
      {children}
    </button>
  );
}
