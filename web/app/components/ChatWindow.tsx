"use client";

import {useState} from "react";
import {ChatMessage} from "../types";

interface ChatWindowProps {
    messages: ChatMessage[];
    onSend: (message: string) => void;
}

export default function ChatWindow({messages, onSend}: ChatWindowProps) {
    const [input, setInput] = useState("");

    function handleSubmit(e: React.FormEvent) {
        e.preventDefault();
        if (!input.trim()) return;
        onSend(input);
        setInput("");
    }

    return (
        <div className="flex flex-col rounded-xl border border-neutral-200 bg-white shadow-sm">
            <ul className="flex max-h-[28rem] flex-col gap-3 overflow-y-auto p-4">
                {messages.length === 0 && (
                    <li className="text-sm text-neutral-400">
                        Please tell me what you would like to support and how much you would like to give.
                    </li>
                )}
                {messages.map((message, index) => (
                    <li
                        key={index}
                        className={`max-w-[80%] rounded-2xl px-4 py-2 text-sm ${
                            message.role === "user"
                                ? "ml-auto bg-blue-600 text-white"
                                : "mr-auto bg-neutral-100 text-neutral-900"
                        }`}
                    >
                        {message.content}
                    </li>
                ))}
            </ul>

            <form onSubmit={handleSubmit} className="flex gap-2 border-t border-neutral-200 p-3">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="I would like to support..."
                    className="flex-1 rounded-full border border-neutral-300 px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button
                    type="submit"
                    className="rounded-full bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
                >
                    Send
                </button>
            </form>
        </div>
    );
}