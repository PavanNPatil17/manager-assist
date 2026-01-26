import { validate } from "uuid";
import { getApiKey } from "@/lib/api-key";
import { Thread } from "@langchain/langgraph-sdk";
import { useQueryState } from "nuqs";
import {
  createContext,
  useContext,
  ReactNode,
  useCallback,
  useState,
  Dispatch,
  SetStateAction,
} from "react";
import { createClient } from "./client";

interface ThreadContextType {
  getThreads: () => Promise<Thread[]>;
  threads: Thread[];
  setThreads: Dispatch<SetStateAction<Thread[]>>;
  threadsLoading: boolean;
  setThreadsLoading: Dispatch<SetStateAction<boolean>>;
}

const ThreadContext = createContext<ThreadContextType | undefined>(undefined);

function getThreadSearchMetadata(
  assistantId: string,
): { graph_id: string } | { assistant_id: string } {
  if (validate(assistantId)) {
    return { assistant_id: assistantId };
  } else {
    return { graph_id: assistantId };
  }
}

export function ThreadProvider({ children }: { children: ReactNode }) {
  const [apiUrlParam] = useQueryState("apiUrl");
  const [assistantIdParam] = useQueryState("assistantId");
  const [threads, setThreads] = useState<Thread[]>([]);
  const [threadsLoading, setThreadsLoading] = useState(false);

  // Use env variables as defaults, fall back to URL params
  const apiUrl = apiUrlParam || process.env.NEXT_PUBLIC_API_URL || null;
  const assistantId = assistantIdParam || process.env.NEXT_PUBLIC_ASSISTANT_ID || null;

  const getThreads = useCallback(async (): Promise<Thread[]> => {
    if (!apiUrl || !assistantId) {
      console.log("Missing apiUrl or assistantId:", { apiUrl, assistantId });
      return [];
    }
    const client = createClient(apiUrl, getApiKey() ?? undefined);

    console.log("Searching threads with assistantId:", assistantId);
    const searchMetadata = getThreadSearchMetadata(assistantId);
    console.log("Search metadata:", searchMetadata);

    try {
      const threads = await client.threads.search({
        metadata: searchMetadata,
        limit: 1000,
      });

      console.log(`Found ${threads.length} threads with metadata filter`);
      
      // If no threads found with metadata filter, try without filter to see if any threads exist
      if (threads.length === 0) {
        console.log("No threads with metadata filter, searching all threads...");
        const allThreads = await client.threads.search({
          limit: 1000,
        });
        console.log(`Total threads in system: ${allThreads.length}`);
        if (allThreads.length > 0) {
          console.log("Sample thread metadata:", allThreads[0].metadata);
        }
      }
      
      // Sort threads by created_at in descending order (newest first)
      return threads.sort((a, b) => {
        const dateA = new Date(a.created_at).getTime();
        const dateB = new Date(b.created_at).getTime();
        return dateB - dateA;
      });
    } catch (error) {
      console.error("Error fetching threads:", error);
      return [];
    }
  }, [apiUrl, assistantId]);

  const value = {
    getThreads,
    threads,
    setThreads,
    threadsLoading,
    setThreadsLoading,
  };

  return (
    <ThreadContext.Provider value={value}>{children}</ThreadContext.Provider>
  );
}

export function useThreads() {
  const context = useContext(ThreadContext);
  if (context === undefined) {
    throw new Error("useThreads must be used within a ThreadProvider");
  }
  return context;
}
