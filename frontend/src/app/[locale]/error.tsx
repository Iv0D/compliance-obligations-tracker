"use client";

import { Alert, Button } from "@/components/ui";

export default function ErrorPage({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  return (
    <div className="space-y-4">
      <Alert variant="error">{error.message || "Something went wrong."}</Alert>
      <Button onClick={reset} variant="secondary">
        Retry
      </Button>
    </div>
  );
}
