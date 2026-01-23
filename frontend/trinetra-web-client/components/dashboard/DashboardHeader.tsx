interface DashboardHeaderProps {
  symbol: string
  price: string
  marketStatus: "open" | "closed"
  lastUpdated: string
}

export function DashboardHeader({
  symbol,
  price,
  marketStatus,
  lastUpdated,
}: DashboardHeaderProps) {
  return (
    <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
      <div>
        <h2 className="text-3xl font-bold text-slate-900 dark:text-white flex items-center gap-3">
          {symbol}
          <span className="text-2xl font-normal text-slate-500 dark:text-slate-400">
            |
          </span>
          <span className="font-mono text-slate-800 dark:text-slate-100">
            {price}
          </span>
        </h2>
        <p className="text-sm text-slate-500 dark:text-slate-400 mt-1 flex items-center gap-1">
          <span
            className={`w-2 h-2 rounded-full ${
              marketStatus === "open" ? "bg-green-500 animate-pulse" : "bg-red-500"
            }`}
          />
          {marketStatus === "open" ? "Market Open" : "Market Closed"}
        </p>
      </div>
      <div className="flex items-center gap-2">
        <span className="text-xs text-slate-400">Last Updated: {lastUpdated}</span>
      </div>
    </div>
  )
}
