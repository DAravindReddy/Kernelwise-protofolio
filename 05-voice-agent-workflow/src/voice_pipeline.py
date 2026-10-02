"""
Real-Time Voice Agent Dialog Pipeline & Tool Calling Engine
"""

import random
import re
import time
from typing import Dict, List, Optional, Tuple
from src.device_tools import check_warranty, schedule_rma_repair, trigger_remote_diagnostics
from src.latency_profiler import LatencyProfiler, TurnLatencyRecord


class VoiceAgentPipeline:
    def __init__(self):
        self.profiler = LatencyProfiler()
        self.turn_counter = 0
        self.context: Dict[str, str] = {
            "serial_number": "",
            "reported_issue": "",
            "booking_slot": "",
        }

    def process_utterance(self, user_audio_or_text: str) -> Tuple[str, TurnLatencyRecord, Optional[Dict]]:
        self.turn_counter += 1
        t_start = time.time()

        # 1. Simulate Streaming STT
        stt_dur = random.uniform(110.0, 150.0)
        time.sleep(stt_dur / 1000.0)
        text = user_audio_or_text.strip()

        # 2. Extract Slots (Serial number, Time, Issue)
        sn_match = re.search(r"\b(SN-[0-9A-Z]+)\b", text, re.IGNORECASE)
        if sn_match:
            self.context["serial_number"] = sn_match.group(1).upper()

        time_match = re.search(r"\b(\d{1,2}(?::\d{2})?\s*(?:am|pm)|tomorrow|monday|friday)\b", text, re.IGNORECASE)
        if time_match:
            self.context["booking_slot"] = time_match.group(1)

        # 3. Simulate LLM Dialog Decision
        llm_dur = random.uniform(140.0, 190.0)
        time.sleep(llm_dur / 1000.0)

        tool_result = None
        tool_dur = 0.0
        response_text = ""

        # Intent: Schedule or Book RMA
        if any(w in text.lower() for w in ["book", "schedule", "appointment", "repair", "rma"]):
            t_tool_start = time.time()
            sn = self.context["serial_number"] or "SN-88210"
            slot = self.context["booking_slot"] or "Tomorrow at 2:00 PM"
            issue = self.context["reported_issue"] or "Device overheating and shutting down"
            tool_result = schedule_rma_repair(sn, issue, slot)
            tool_dur = (time.time() - t_tool_start) * 1000.0 + random.uniform(25.0, 40.0)
            response_text = f"I have scheduled your field repair appointment for {slot}. Your tracking ticket is {tool_result['ticket_id']}."

        # Intent: Diagnostic Check
        elif any(w in text.lower() for w in ["diagnose", "health", "temperature", "check my device", "overheating"]):
            t_tool_start = time.time()
            sn = self.context["serial_number"] or "SN-88210"
            tool_result = trigger_remote_diagnostics(sn)
            tool_dur = (time.time() - t_tool_start) * 1000.0 + random.uniform(30.0, 45.0)
            if tool_result["errors"]:
                response_text = f"I ran remote diagnostics on device {sn}. The SoC temperature is {tool_result['temperature_c']}°C with active fault code {tool_result['errors'][0]}. Would you like me to book a technician?"
            else:
                response_text = f"Remote diagnostics for device {sn} show all parameters normal: SoC is {tool_result['temperature_c']}°C with battery health at {tool_result['battery_health']}%."

        # Intent: Warranty
        elif any(w in text.lower() for w in ["warranty", "coverage", "guarantee"]):
            t_tool_start = time.time()
            sn = self.context["serial_number"] or "SN-88210"
            tool_result = check_warranty(sn)
            tool_dur = (time.time() - t_tool_start) * 1000.0 + random.uniform(20.0, 35.0)
            response_text = f"Device {sn} has {tool_result['tier']} warranty status ({tool_result['status']}), valid through {tool_result['expires']}."

        else:
            response_text = "Hello! I am the Kernelwise Device Support Voice Assistant. You can ask me to run remote diagnostics, verify warranty coverage, or schedule an RMA repair."

        # 4. Simulate Streaming TTS Chunk Synthesis
        tts_dur = random.uniform(95.0, 130.0)
        time.sleep(tts_dur / 1000.0)

        record = self.profiler.log_turn(
            turn_id=self.turn_counter,
            stt=stt_dur,
            llm=llm_dur,
            tool=tool_dur,
            tts=tts_dur,
        )

        return response_text, record, tool_result
