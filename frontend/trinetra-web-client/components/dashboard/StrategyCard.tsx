import { ArrowUpRight, ArrowDownRight } from "lucide-react"

interface Target {
  label: string
  value: string
}

interface StrategyCardProps {
  type: "buy" | "sell"
  entry: string
  stopLoss: string
  targets: Target[]
}

export function StrategyCard({
  type,
  entry,
  stopLoss,
  targets,
}: StrategyCardProps) {
  const isBuy = type === "buy"

  const borderColor = isBuy
    ? "border-slate-200 dark:border-slate-700"
    : "border-red-200 dark:border-red-900/50"

  const accentColor = isBuy ? "bg-emerald-500" : "bg-red-500"

  const headerBg = isBuy
    ? "bg-emerald-50/30 dark:bg-emerald-900/10"
    : "bg-red-50/30 dark:bg-red-900/10"

  const headerBorder = isBuy
    ? "border-slate-100 dark:border-slate-700/50"
    : "border-red-100 dark:border-red-900/30"

  const titleColor = isBuy
    ? "text-emerald-700 dark:text-emerald-400"
    : "text-red-700 dark:text-red-400"

  const iconColor = isBuy ? "text-emerald-500" : "text-red-500"

  const targetColor = isBuy
    ? "text-emerald-600 dark:text-emerald-500"
    : "text-red-600 dark:text-red-500"

  const Icon = isBuy ? ArrowUpRight : ArrowDownRight

  const ringClass = isBuy
    ? ""
    : "ring-1 ring-red-500/20 dark:ring-red-500/10"

  return (
    <div
      className={`group relative bg-white dark:bg-slate-800 rounded-xl border ${borderColor} shadow-sm overflow-hidden flex flex-col h-full ${ringClass}`}
    >
      <div className={`absolute top-0 left-0 w-1 h-full ${accentColor}`} />
      <div
        className={`p-4 border-b ${headerBorder} ${headerBg}`}
      >
        <div className="flex justify-between items-center">
          <span
            className={`text-sm font-bold ${titleColor} uppercase tracking-wide`}
          >
            {isBuy ? "Buy Strategy" : "Sell Strategy"}
          </span>
          <Icon className={`h-4 w-4 ${iconColor}`} />
        </div>
      </div>
      <div className="p-5 space-y-4 flex-1">
        <div className="flex justify-between items-end">
          <div>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Entry {isBuy ? "Above" : "Below"}
            </p>
            <p className="text-xl font-bold text-slate-800 dark:text-white">
              {entry}
            </p>
          </div>
          <div className="text-right">
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Stop Loss
            </p>
            <p className="text-lg font-bold text-red-500">{stopLoss}</p>
          </div>
        </div>
        <div className="h-px bg-slate-100 dark:bg-slate-700" />
        <div className="grid grid-cols-3 gap-y-2 text-sm">
          {targets.map((target, index) => (
            <div
              key={target.label}
              className={`text-slate-600 dark:text-slate-300 ${
                index === targets.length - 1 ? "col-span-2" : ""
              }`}
            >
              <span
                className={`${
                  index === targets.length - 1 ? "font-bold" : "font-semibold"
                } ${targetColor}`}
              >
                {target.label}:
              </span>{" "}
              {target.value}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
