import { TrendingUp } from "lucide-react"

interface MovingAverage {
  period: string
  value: string
  isPositive: boolean
}

interface MovingAveragesProps {
  averages: MovingAverage[]
}

export function MovingAverages({ averages }: MovingAveragesProps) {
  return (
    <div className="space-y-3">
      <div className="flex items-center gap-2">
        <TrendingUp className="h-4 w-4 text-slate-400" />
        <h3 className="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
          Key Moving Averages (Trend Support)
        </h3>
      </div>
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
        {averages.map((avg) => (
          <div
            key={avg.period}
            className="bg-white dark:bg-slate-800 p-3 rounded-lg border border-slate-200 dark:border-slate-700 text-center shadow-sm"
          >
            <p className="text-[10px] text-slate-400 mb-1">{avg.period}</p>
            <p
              className={`font-bold ${
                avg.isPositive
                  ? "text-green-600 dark:text-green-400"
                  : "text-red-600 dark:text-red-400"
              }`}
            >
              {avg.value}
            </p>
          </div>
        ))}
      </div>
    </div>
  )
}
