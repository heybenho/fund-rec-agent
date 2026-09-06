"use client";

import {useState} from "react";
import {DonorProfile} from "../types";

interface DonorFormProps {
    onSubmit: (profile: DonorProfile) => void;
}

export default function DonorForm({onSubmit}: DonorFormProps) {
    const [interest, setInterest] = useState("");
    const [capacity, setCapacity] = useState("");
    const [unit, setUnit] = useState("");
    const [purpose, setPurpose] = useState("");

    function handleSubmit(e: React.FormEvent) {
        e.preventDefault();
        onSubmit({
            interest,
            capacity: Number(capacity),
            unit: unit || undefined,
            purpose: purpose || undefined,
        })
    }

    return (
        <form onSubmit={handleSubmit}>
            <label>
                What are you interested in supporting?
                <textarea
                    value = {interest}
                    onChange = {(e) => setInterest(e.target.value)}
                    required
                /> 
            </label>

            <label>
                Giving capacity ($)
                <input
                    type = "number"
                    value = {capacity}
                    onChange = {(e) => setCapacity(e.target.value)}
                    required
                />
            </label>

            <label>
                Unit (optional)
                <input
                    type = "text"
                    value = {unit}
                    onChange = {(e) => setUnit(e.target.value)}
                    placeholder = "e.g. chancellor.engineering"
                />
            </label>

            <label>
                Purpose (optional)
                <input
                    type = "text"
                    value = {purpose}
                    onChange = {(e) => setPurpose(e.target.value)}
                    placeholder = "e.g. grad_support"
                />
            </label>

            <button type = "submit"> Find matching funds </button>
        </form>
    );
}