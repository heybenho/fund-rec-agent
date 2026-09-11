"use client";

import {useState} from "react";
import ChatWindow from "./components/ChatWindow";
import {ChatMessage, FundRecommendation} from "./types";
import RecommendationList from "./components/RecommendationList";

export default function Home() {
  const [messages, setMessages] = useState<ChatMessage[]>([{role: "assistant", content: "Please tell me what you would like to support and how much you would like to give."}]);
  const [recommendations, setRecommendations] = useState<FundRecommendation[]>([]);


  async function handleSend(content: string) {
    const nextMessages: ChatMessage[] = [...messages, {role: "user", content}];
    setMessages(nextMessages);

    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({messages: nextMessages}),
    });

    if (!response.ok) {
      setMessages([...nextMessages, {role: "assistant", content: "Sorry, something went wrong reaching the agent."}]);
      return;
    }

    const data = await response.json();
    setMessages([...nextMessages, {role: "assistant", content: data.reply}]);
    setRecommendations(data.recommendations);
  }

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-2xl flex-col gap-6 px-4 py-10">
      <h1 className="text-2xl font-semibold text-neutral-900">Fund Recommendation Agent</h1>
      <ChatWindow messages={messages} onSend={handleSend} />
      <RecommendationList recommendations={recommendations} />
    </main>
  );
}