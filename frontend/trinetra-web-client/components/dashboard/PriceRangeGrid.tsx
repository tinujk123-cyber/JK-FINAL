interface PriceLevel {
  label: string
  value: string
}

interface PriceRangeGridProps {
  levels: PriceLevel[]
}

export function PriceRangeGrid({ levels }: PriceRangeGridProps) {
  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      {levels.map((level) => (
        <div
          key={level.label}
          className="bg-slate-50 dark:bg-slate-800/50 p-3 rounded-lg border border-slate-200 dark:border-slate-700/50 text-center"
        >
          <p className="text-[10px] font-bold text-slate-400 uppercase">
            {level.label}
          </p>
          <p className="text-base font-bold text-slate-800 dark:text-slate-200">
            {level.value}
          </p>
        </div>
      ))}
    </div>
  )
}
