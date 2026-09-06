"use client";

import {useState} from "react";
import DonorForm from "./components/DonorForm";
import {DonorProfile, FundRecommendation} from "./types";
import RecommendationList from "./components/RecommendationList";

export default function Home() {
  const [recommendations, setRecommendations] = useState<FundRecommendation[]>([]);

  async function handleSubmit(profile: DonorProfile) {
    const response = await fetch("/api/recommend", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(profile),
    });

    const data: FundRecommendation[] = await response.json();
    setRecommendations(data);
  }

  return (
    <main>
      <h1>Fund Recommendation Agent</h1>
      <DonorForm onSubmit = {handleSubmit} />
      <RecommendationList recommendations={recommendations}/>
    </main>
  );
}