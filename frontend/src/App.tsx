import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { Dashboard } from "./pages/Dashboard";
import { Agents }    from "./pages/Agents";
import { Insights }  from "./pages/Insights";
import { Layout }    from "./components/Layout";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: 1, staleTime: 30_000 },
  },
});

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="agents"    element={<Agents />} />
            <Route path="insights"  element={<Insights />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}