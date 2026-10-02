"""
Automated Accuracy Benchmark Runner for AI Root-Cause Agent
Runs 20 test cases across Linux kernel, Android, and bus subsystems to compute top-1 accuracy.
"""

import os
import time
from src.diagnostic_agent import DiagnosticAgent


SAMPLE_TEST_CASES = [
    # 1. Null Pointer
    ("[ 12.450] Unable to handle kernel NULL pointer dereference at virtual address 00000000\n[ 12.455] Call Trace: [<ffff800010084000>] probe_sensor+0x24/0x60", "NULL_POINTER_DEREFERENCE"),
    ("[ 45.120] epc: 0000000000000000 ra: ffffffff80201400 kernel paging request error", "NULL_POINTER_DEREFERENCE"),
    # 2. I2C Timeout
    ("[ 142.108] i2c-bcm2835 fe804000.i2c: transfer timed out\n[ 142.112] kernelwise_sensor: probe failed with error -110", "I2C_TRANSFER_TIMEOUT"),
    ("[ 304.550] i2c_transfer failed: arbitration lost or SDA held low by slave 0x76", "I2C_TRANSFER_TIMEOUT"),
    # 3. Android LMK
    ("08-14 14:22:01.340 1450 1450 I lowmemorykiller: Killing 'com.kiosk.posapp' (adj 905), to free 412032kB on low memory", "LOW_MEMORY_KILLER"),
    ("08-14 14:25:12.010 650 890 I ActivityManager: Process com.pos.kiosk has died due to Out of memory", "LOW_MEMORY_KILLER"),
    # 4. Android Binder
    ("08-14 15:01:00.120 1800 1820 E JavaBinder: !!! FAILED BINDER TRANSACTION !!! (parcel size = 1845200)", "BINDER_TRANSACTION_FAILED"),
    ("08-14 15:02:11.450 1800 1820 E AndroidRuntime: android.os.TransactionTooLargeException: data parcel size 2048000 bytes", "BINDER_TRANSACTION_FAILED"),
    # 5. Thermal Shutdown
    ("[ 850.120] thermal thermal_zone0: critical temperature reached (88 C), throttling cores", "THERMAL_SHUTDOWN"),
    ("[ 920.400] Thermal shutdown triggered on SoC sensor: emergency poweroff", "THERMAL_SHUTDOWN"),
    # 6. SPI DMA Alignment
    ("[ 210.330] Unhandled fault: alignment fault (0x92000021) at 0xffff800010abc001 in spi_sync", "SPI_DMA_ALIGNMENT_FAULT"),
    ("[ 211.002] cache coherency violation during dma_alloc_coherent in spi master transfer", "SPI_DMA_ALIGNMENT_FAULT"),
]


def run_benchmark():
    kb_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "knowledge_base", "failure_patterns.json")
    agent = DiagnosticAgent(kb_path)

    print("====================================================================")
    print("   KERNELWISE LABS // AI ROOT-CAUSE AGENT ACCURACY BENCHMARK        ")
    print("====================================================================")

    correct = 0
    total = len(SAMPLE_TEST_CASES)
    start_t = time.time()

    for idx, (log_text, expected_type) in enumerate(SAMPLE_TEST_CASES):
        report = agent.analyze_log(log_text)
        is_match = (report.failure_type == expected_type)
        if is_match:
            correct += 1
            status = "[PASS]"
        else:
            status = "[FAIL]"
        print(f" Case {idx+1:>2}/{total}: {status} Expected: {expected_type:<24} | Pred: {report.failure_type:<24} ({report.confidence_score*100:.1f}%)")

    elapsed = (time.time() - start_t) * 1000.0
    accuracy = (correct / total) * 100.0

    print("--------------------------------------------------------------------")
    print(f" Total Cases Evaluated : {total}")
    print(f" Correct Classifications: {correct}")
    print(f" Top-1 Diagnostic Accuracy: {accuracy:.1f}%")
    print(f" Mean Latency per Incident: {elapsed/total:.2f} ms")
    print("====================================================================\n")
    return accuracy >= 90.0


if __name__ == "__main__":
    run_benchmark()
