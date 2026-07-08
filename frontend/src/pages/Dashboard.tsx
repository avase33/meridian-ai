import { useQuery } from "@tanstack/react-query";
import { AlertTriangle, Activity, CheckCircle2, TrendingUp } from "lucide-react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from "recharts";

const API = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

interface Insight {
  id:            string;
  severity:      "critical" | "high" | "medium" | "low";
  metric_name:   string;
  deviation_pct: number;
  root_cause:    string;
  created_at:    string;
}

interface StatCard {
  label:  string;
  value:  string | number;
  delta?: string;
  icon:   React.ReactNode;
  color:  string;
}

function StatCard({ label, value, delta, icon, color }: StatCard) {
  return (
    <div className="rounded-xl border border-gray-800 bg-gray-900 p-5 shadow-sm">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-gray-400">{label}</p>
          <p className="mt-1 text-3xl font-bold text-white">{value}</p>
          {delta && <p className="mt-1 text-xs text-gray-500">{delta}</p>}
        </div>
        <span className={`rounded-lg p-2 ${color}`}>{icon}</span>
      </div>
    </div>
  );
}

export function Dashboard() {
  const { data: insights = [] } = useQuery<Insight[]>({
    queryKey: ["insights"],
    queryFn:  () => fetch(`${API}/api/v1/insights?limit=5`).then(r => r.json()),
  });

  const criticalCount = insights.filter(i => i.severity === "critical").length;
  const mockChartData = Array.from({ length: 12 }, (_, i) => ({
    time:  `${String(i * 2).padStart(2, "0")}:00`,
    value: 80_000 + Math.random() * 20_000,
  }));

  return (
    <div className="space-y-8 p-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Overview</h1>
        <p className="mt-1 text-gray-400">
          Meridian is watching your business — here is what matters right now.
        </p>
      </div>

      {/* Stat cards */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard label="Active Agents"   value={12}          delta="+2 this week"      icon={<Activity size={18} />}      color="bg-blue-900/40 text-blue-400" />
        <StatCard label="Insights Today"  value={insights.length} delta="last updated now" icon={<TrendingUp size={18} />}   color="bg-purple-900/40 text-purple-400" />
        <StatCard label="Critical Alerts" value={criticalCount} delta="requires action"   icon={<AlertTriangle size={18} />} color="bg-red-900/40 text-red-400" />
        <StatCard label="Resolved"        value={47}          delta="last 7 days"        icon={<CheckCircle2 size={18} />}  color="bg-green-900/40 text-green-400" />
      </div>

      {/* Chart */}
      <div className="rounded-xl border border-gray-800 bg-gray-900 p-6">
        <h2 className="mb-4 text-lg font-semibold text-white">Revenue — Last 24h</h2>
        <ResponsiveContainer width="100%" height={240}>
          <LineChart data={mockChartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis dataKey="time" tick={{ fill: "#9ca3af", fontSize: 11 }} />
            <YAxis tickFormatter={v => `$${(v/1000).toFixed(0)}k`} tick={{ fill: "#9ca3af", fontSize: 11 }} />
            <Tooltip
              contentStyle={{ background: "#111827", border: "1px solid #374151", borderRadius: 8 }}
              labelStyle={{ color: "#fff" }}
              formatter={(v: number) => [`$${v.toFixed(0)}`, "Revenue"]}
            />
            <Line type="monotone" dataKey="value" stroke="#8b5cf6" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Insight feed */}
      <div className="rounded-xl border border-gray-800 bg-gray-900 p-6">
        <h2 className="mb-4 text-lg font-semibold text-white">Recent Insights</h2>
        {insights.length === 0 ? (
          <p className="text-gray-500">No insights yet — agents are monitoring.</p>
        ) : (
          <ul className="divide-y divide-gray-800">
            {insights.map(i => (
              <li key={i.id} className="py-3">
                <div className="flex items-center gap-3">
                  <span className={`inline-flex h-2 w-2 rounded-full ${
                    i.severity === "critical" ? "bg-red-500" :
                    i.severity === "high"     ? "bg-orange-500" :
                    i.severity === "medium"   ? "bg-yellow-500" : "bg-green-500"
                  }`} />
                  <span className="font-medium text-white">{i.metric_name}</span>
                  <span className="text-sm text-gray-400">
                    {i.deviation_pct?.toFixed(1)}% deviation
                  </span>
                </div>
                <p className="mt-1 pl-5 text-sm text-gray-500 line-clamp-2">{i.root_cause}</p>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}