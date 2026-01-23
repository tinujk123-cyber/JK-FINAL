interface PivotLevel {
  label: string
  value: string
  isPivot?: boolean
}

interface PivotLevelsProps {
  levels: PivotLevel[]
}

export function PivotLevels({ levels }: PivotLevelsProps) {
  return (
    <div className="bg-amber-50/50 dark:bg-amber-900/10 rounded-xl border border-amber-100 dark:border-amber-900/30 p-1">
      <div className="grid grid-cols-5 gap-1 md:gap-4 divide-x divide-amber-200/50 dark:divide-amber-800/30">
        {levels.map((level) => (
          <div
            key={level.label}
            className={`text-center p-2 ${
              level.isPivot ? "bg-amber-100/50 dark:bg-amber-900/30 rounded" : ""
            }`}
          >
            <p
              className={`text-[10px] font-bold uppercase ${
                level.isPivot
                  ? "text-amber-700 dark:text-amber-400"
                  : "text-amber-600/70 dark:text-amber-500/70"
              }`}
            >
              {level.label}
            </p>
            <p
              className={`text-sm font-bold ${
                level.isPivot
                  ? "text-slate-900 dark:text-white"
                  : "text-slate-800 dark:text-amber-100"
              }`}
            >
              {level.value}
            </p>
          </div>
        ))}
      </div>
    </div>
  )
}
