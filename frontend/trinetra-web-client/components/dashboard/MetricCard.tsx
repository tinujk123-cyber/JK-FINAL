import { ArrowDown, LucideIcon } from "lucide-react"
import { ReactNode } from "react"

interface MetricCardProps {
  label: string
  value: string | ReactNode
  valueClassName?: string
  icon?: LucideIcon
}

export function MetricCard({
  label,
  value,
  valueClassName = "text-xl font-bold text-slate-900 dark:text-white font-mono",
  icon: Icon,
}: MetricCardProps) {
  return (
    <div className="bg-white dark:bg-slate-800 p-4 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm hover:shadow-md transition-shadow">
      <p className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">
        {label}
      </p>
      <div className={valueClassName}>
        {typeof value === "string" ? (
          <p className="flex items-center gap-1">
            {value}
            {Icon && <Icon className="h-4 w-4" />}
          </p>
        ) : (
          value
        )}
      </div>
    </div>
  )
}

interface SmartMoneyValueProps {
  status: string
}

export function SmartMoneyValue({ status }: SmartMoneyValueProps) {
  return (
    <p className="text-lg font-bold text-red-600 dark:text-red-400 flex items-center gap-1">
      {status}
      <ArrowDown className="h-4 w-4" />
    </p>
  )
}

interface TrendValueProps {
  trend: string
  description: string
}

export function TrendValue({ trend, description }: TrendValueProps) {
  return (
    <div className="flex flex-col">
      <p className="text-lg font-bold text-red-600 dark:text-red-400">{trend}</p>
      <p className="text-xs text-red-500/70 dark:text-red-400/60 font-medium">
        {description}
      </p>
    </div>
  )
}
