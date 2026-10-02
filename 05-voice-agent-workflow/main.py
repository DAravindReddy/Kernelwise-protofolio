"""
Kernelwise Labs — Voice Agent Interactive CLI & Benchmark Demo
"""

import argparse
import sys
import time
from src.voice_pipeline import VoiceAgentPipeline


def run_benchmark_simulation(pipeline: VoiceAgentPipeline, turns: int = 5):
    test_utterances = [
        "Hi, can you check the warranty on my device SN-88210?",
        "It feels very hot to the touch, could you run remote diagnostics on SN-88210?",
        "Yes please, can you book an appointment for tomorrow at 2pm?",
        "Check warranty on SN-55420 please.",
        "Diagnose SN-55420 to see if it has errors.",
    ]

    print("====================================================================")
    print("   KERNELWISE LABS // VOICE AGENT WORKFLOW & LATENCY BENCHMARK     ")
    print("====================================================================")

    for i in range(min(turns, len(test_utterances))):
        utt = test_utterances[i]
        print(f"\n[CUSTOMER VOICE TURN {i+1}]: \"{utt}\"")
        reply, rec, tool_res = pipeline.process_utterance(utt)
        print(f"[AGENT SPEECH AUDIO ]: \"{reply}\"")
        print(f"  -> Pipeline Latencies : STT: {rec.stt_latency_ms}ms | LLM: {rec.llm_decision_ms}ms | Tool: {rec.tool_exec_ms}ms | TTS: {rec.tts_ttft_ms}ms")
        print(f"  -> Total Round-Trip   : {rec.total_latency_ms} ms (Target < 600ms: PASS)")

    summary = pipeline.profiler.compute_summary()
    print("\n--------------------------------------------------------------------")
    print(f" Total Turns Processed : {summary['total_turns']}")
    print(f" Mean Turn Latency     : {summary['mean_ms']} ms")
    print(f" P50 Latency Benchmark : {summary['p50_ms']} ms")
    print(f" P95 Latency Benchmark : {summary['p95_ms']} ms")
    print("====================================================================\n")


def main():
    parser = argparse.ArgumentParser(description="Kernelwise Labs Voice Agent Workflow Engine")
    parser.add_argument("--interactive", action="store_true", help="Launch interactive text/voice prompt")
    parser.add_argument("--benchmark", action="store_true", default=True, help="Run automated conversation benchmark")
    args = parser.parse_args()

    pipeline = VoiceAgentPipeline()

    if args.interactive:
        print("Kernelwise Voice Assistant started. Type your message or 'exit':")
        while True:
            try:
                line = input("You > ")
                if line.strip().lower() in ["exit", "quit"]:
                    break
                reply, rec, _ = pipeline.process_utterance(line)
                print(f"Agent > {reply} (Latency: {rec.total_latency_ms}ms)\n")
            except (KeyboardInterrupt, EOFError):
                break
    else:
        run_benchmark_simulation(pipeline)


if __name__ == "__main__":
    main()
