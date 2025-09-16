// frontend/components/InputField.tsx
import React from 'react';

interface InputFieldProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
}

export default function InputField({ label, ...props }: InputFieldProps) {
  return (
    <div className="flex flex-col space-y-1">
      <label className="font-semibold">{label}</label>
      <input
        className="p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        {...props}
      />
    </div>
  );
}
