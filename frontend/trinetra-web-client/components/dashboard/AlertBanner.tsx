import { AlertTriangle } from "lucide-react"

interface AlertBannerProps {
  type: "buy" | "sell"
  message: string
}

export function AlertBanner({ type, message }: AlertBannerProps) {
  const bgColor =
    type === "sell"
      ? "bg-red-50 dark:bg-red-950/40 border-red-200 dark:border-red-900"
      : "bg-green-50 dark:bg-green-950/40 border-green-200 dark:border-green-900"

  const textColor =
    type === "sell"
      ? "text-red-700 dark:text-red-500"
      : "text-green-700 dark:text-green-500"

  const iconColor =
    type === "sell"
      ? "text-red-600 dark:text-red-500"
      : "text-green-600 dark:text-green-500"

  return (
    <div
      className={`w-full rounded-xl ${bgColor} border p-4 shadow-sm flex items-center justify-center gap-3 animate-pulse`}
    >
      <AlertTriangle className={`${iconColor} h-8 w-8`} />
      <span
        className={`text-xl md:text-2xl font-bold ${textColor} tracking-wide uppercase`}
      >
        {message}
      </span>
    </div>
  )
}
