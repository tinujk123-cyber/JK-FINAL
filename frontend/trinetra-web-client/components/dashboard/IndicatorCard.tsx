interface ADXIndicatorProps {
  value: number
  strength: string
}

export function ADXIndicator({ value, strength }: ADXIndicatorProps) {
  return (
    <div className="bg-white dark:bg-slate-800 rounded-xl border border-amber-200 dark:border-amber-700/50 p-4 shadow-sm flex flex-col justify-center items-center text-center">
      <p className="text-xs font-bold text-slate-400 uppercase tracking-wide mb-2">
        ADX Strength
      </p>
      <div className="text-2xl font-bold text-slate-800 dark:text-slate-100 mb-1">
        {value}{" "}
        <span className="text-sm font-medium text-amber-500">({strength})</span>
      </div>
      <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2 mt-2">
        <div
          className="bg-amber-400 h-2 rounded-full"
          style={{ width: `${value}%` }}
        />
      </div>
      <p className="text-[10px] text-slate-400 mt-2">Weak Trend Detected</p>
    </div>
  )
}

interface RSIIndicatorProps {
  value: number
  status: string
}

export function RSIIndicator({ value, status }: RSIIndicatorProps) {
  return (
    <div className="flex flex-col rounded-xl overflow-hidden shadow-sm border border-red-200 dark:border-red-900/50">
      <div className="bg-red-600 text-white text-center py-1.5 text-xs font-bold uppercase tracking-widest">
        Reversal Zone
      </div>
      <div className="bg-white dark:bg-slate-800 p-4 flex flex-col justify-center items-center text-center flex-1">
        <p className="text-xs font-bold text-slate-400 uppercase tracking-wide mb-2">
          RSI Momentum
        </p>
        <div className="text-2xl font-bold text-slate-800 dark:text-slate-100 mb-1">
          {value}
        </div>
        <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2 mt-2 relative">
          <div className="absolute left-[30%] top-0 bottom-0 w-px bg-slate-400 dark:bg-slate-500 h-3 -mt-0.5" />
          <div className="absolute left-[70%] top-0 bottom-0 w-px bg-slate-400 dark:bg-slate-500 h-3 -mt-0.5" />
          <div
            className="bg-red-500 h-2 rounded-full"
            style={{ width: `${value}%` }}
          />
        </div>
        <p className="text-[10px] text-red-500 mt-2 font-bold uppercase">
          {status}
        </p>
      </div>
    </div>
  )
}
