"use client";

import { useState, useRef } from "react";
import Image from "next/image";

interface SearchResult {
  child_id: string;
  parent_id: string;
  child_content: string;
  parent_content: string;
  header: string;
  score: number;
}

export default function Home() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [isSearching, setIsSearching] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<string | null>(null);
  const [answer, setAnswer] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    setUploadStatus("Uploading and indexing document...");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${API_URL}/ingestion/upload`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Upload failed");

      const data = await response.json();
      setUploadStatus(`Success: ${data.filename} ingested!`);
      setTimeout(() => setUploadStatus(null), 5000);
    } catch (err) {
      setUploadStatus("Error: Failed to ingest document.");
      console.error(err);
    } finally {
      setIsUploading(false);
    }
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsSearching(true);
    try {
      const response = await fetch(`${API_URL}/search/?q=${encodeURIComponent(query)}&top_k=5`);
      if (!response.ok) throw new Error("Search failed");

      const data = await response.json();
      setResults(data.results);
      setAnswer(data.answer);
    } catch (err) {
      console.error(err);
    } finally {
      setIsSearching(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#09090b] text-zinc-100 selection:bg-indigo-500/30">
      {/* Header */}
      <header className="border-b border-white/5 bg-black/20 backdrop-blur-xl sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center shadow-lg shadow-indigo-500/20">
              <span className="text-white font-bold text-lg">O</span>
            </div>
            <h1 className="text-xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white to-zinc-400">
              OrchestrAI
            </h1>
          </div>
          <div className="flex items-center gap-4">
             <div className="flex items-center gap-2 px-3 py-1 bg-emerald-500/10 border border-emerald-500/20 rounded-full">
               <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse" />
               <span className="text-[10px] uppercase tracking-wider font-bold text-emerald-500">System Live</span>
             </div>
             <button 
               onClick={() => fileInputRef.current?.click()}
               disabled={isUploading}
               className="text-sm font-medium px-4 py-2 bg-white text-black rounded-lg hover:bg-zinc-200 transition-colors disabled:opacity-50"
             >
               {isUploading ? "Processing..." : "Upload Research"}
             </button>
             <input 
               type="file" 
               ref={fileInputRef} 
               onChange={handleUpload} 
               className="hidden" 
               accept=".pdf"
             />
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-6 py-20">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h2 className="text-4xl font-extrabold mb-4 tracking-tight">
            Multi-Agent Intelligence <br />
            <span className="text-zinc-500">at your fingertips.</span>
          </h2>
          <p className="text-zinc-400 max-w-xl mx-auto">
            Search across your research library with semantic precision. Powered by Gemini 1.5 Pro and LangGraph.
          </p>
        </div>

        {/* Search Bar */}
        <div className="relative group max-w-2xl mx-auto mb-16">
          <div className="absolute -inset-1 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-2xl blur opacity-25 group-focus-within:opacity-50 transition duration-1000 group-focus-within:duration-200"></div>
          <form onSubmit={handleSearch} className="relative flex items-center">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.setQuery ? e.target.value : e.target.value)}
              placeholder="Ask anything about your documents..."
              className="w-full h-14 bg-zinc-900 border border-white/10 rounded-xl px-6 text-lg focus:outline-none focus:border-indigo-500/50 transition-all"
            />
            <button 
              type="submit"
              disabled={isSearching}
              className="absolute right-3 px-4 py-1.5 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-500 transition-colors"
            >
              {isSearching ? "..." : "Search"}
            </button>
          </form>
        </div>

        {/* AI Answer Section */}
        {results.length > 0 && (
          <div className="mb-12 animate-in fade-in slide-in-from-bottom-4 duration-700">
            <div className="p-8 bg-gradient-to-br from-indigo-500/10 via-purple-500/5 to-transparent border border-white/10 rounded-3xl shadow-2xl backdrop-blur-sm relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-4 opacity-20 group-hover:opacity-40 transition-opacity">
                <div className="w-20 h-20 bg-indigo-500 rounded-full blur-3xl" />
              </div>
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 bg-indigo-500 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-500/30">
                  <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <div>
                  <h3 className="text-lg font-bold text-white">AI Synthesis</h3>
                  <p className="text-[10px] uppercase tracking-widest text-indigo-400 font-bold">OrchestrAI Agent v1.0</p>
                </div>
              </div>
              <div className="prose prose-invert max-w-none">
                  <p className="text-zinc-200 leading-relaxed text-lg font-medium whitespace-pre-wrap">
                    {answer}
                  </p>
              </div>
            </div>
          </div>
        )}

        {uploadStatus && (
          <div className="mb-8 p-4 bg-indigo-500/10 border border-indigo-500/20 rounded-xl text-indigo-400 text-center text-sm font-medium animate-in fade-in slide-in-from-top-4">
            {uploadStatus}
          </div>
        )}

        {/* Results */}
        <div className="space-y-6">
          {results.length > 0 ? (
            results.map((res, i) => (
              <div 
                key={i} 
                className="group p-6 bg-zinc-900/50 border border-white/5 rounded-2xl hover:border-white/10 transition-all duration-300"
              >
                <div className="flex items-center gap-2 mb-3">
                  <span className="text-[10px] uppercase tracking-widest font-bold text-zinc-500 bg-white/5 px-2 py-0.5 rounded">
                    {res.header}
                  </span>
                </div>
                <p className="text-zinc-300 leading-relaxed mb-4 italic text-sm">
                  "...{res.child_content}..."
                </p>
                <div className="p-4 bg-black/40 rounded-xl border border-white/5">
                  <p className="text-zinc-400 text-sm line-clamp-3">
                    {res.parent_content}
                  </p>
                </div>
              </div>
            ))
          ) : query && !isSearching ? (
            <div className="text-center py-20 text-zinc-500">
              No relevant intelligence found for this query.
            </div>
          ) : null}
        </div>
      </main>
    </div>
  );
}
