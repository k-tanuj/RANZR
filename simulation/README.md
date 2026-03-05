# 🧪 RANZR Attack Simulator

Safe ransomware behavior emulator for testing the RANZR detection system **without using actual malware**.

## Purpose

This simulator creates ransomware-like behavior patterns to test and demonstrate:
- Real-time monitoring system
- AI anomaly detection
- Threat scoring engine
- Automated response mechanisms

## What It Simulates

### 1. File Encryption Behavior
- Rapid file modifications (simulates encryption process)
- Mass file renaming (adds `.locked` extension)
- Typical ransomware file access patterns

### 2. System Resource Abuse
- CPU spike generation (encryption overhead)
- Memory pressure simulation
- Process creation anomalies

### 3. File System Chaos
- High file creation/deletion rates
- Temporary file generation
- Abnormal I/O patterns

## Usage

### Basic Usage (Medium Intensity)
```powershell
# Terminal 1: Start monitoring system
python -m monitoring.file_monitor

# Terminal 2: Start attack simulation
python -m simulation.attack_simulator
```

### Custom Intensity Levels

**Low Intensity** (for testing baseline):
```powershell
python -m simulation.attack_simulator --intensity low
```

**High Intensity** (for stress testing):
```powershell
python -m simulation.attack_simulator --intensity high
```

## Expected Monitoring Output

When simulator is running, you should see spikes in:

```
file_modification_rate: 30-50  (normal: 0-3)
rename_count: 15-30            (normal: 0-2)
cpu_usage_percent: 85-95       (normal: 5-20)
process_spike: 2-5             (normal: 0-1)
```

## Safety

✅ **This is NOT real malware**
- No actual encryption
- No data destruction
- No network activity
- No system file access
- Easy to stop (Ctrl+C)

All activity is confined to `test_folder/` only.

## Demo Script for Judges

### Setup (30 seconds)
```powershell
# Terminal 1
cd D:\RANZR-main\RANZR
.\venv\Scripts\Activate.ps1
python -m monitoring.file_monitor
```

Wait for baseline to show normal behavior (all zeros).

### Attack Demo (1 minute)
```powershell
# Terminal 2
cd D:\RANZR-main\RANZR
.\venv\Scripts\Activate.ps1
python -m simulation.attack_simulator --intensity high
```

### What to Show Judges

1. **Before Attack**: Show normal metrics (Terminal 1)
   - `file_modification_rate: 0`
   - `rename_count: 0`
   - `cpu_usage_percent: 5-10`

2. **During Attack**: Show spike detection
   - `file_modification_rate: 40+`
   - `rename_count: 20+`
   - `cpu_usage_percent: 90+`

3. **Stop Attack**: Ctrl+C in Terminal 2
   - Metrics return to normal
   - Show baseline learning capability

### Key Talking Points

> "Instead of using actual ransomware, which would be dangerous, we built a safe simulator that mimics real ransomware behavior patterns. This allows us to demonstrate real-time detection without any security risks."

> "Notice how our AI system immediately detects the abnormal file modification rate and CPU spikes, which are classic ransomware indicators."

> "The threat scoring engine combines multiple signals - file entropy, modification patterns, CPU usage, and process anomalies - to accurately identify the attack."

## Troubleshooting

### Simulator Not Creating Spikes?
- Check if `test_folder/` exists
- Verify monitoring is watching correct folder
- Try `--intensity high`

### CPU Not Spiking?
- Close other heavy applications
- Check Task Manager during simulation
- May be less visible on high-end systems

### Files Not Being Modified?
- Check file permissions on `test_folder/`
- Ensure no antivirus is blocking the script
- Look for error messages in simulator output

## Integration with Full Pipeline

To test the **complete AI detection pipeline**:

```powershell
# This will:
# 1. Train AI model
# 2. Analyze entropy
# 3. Calculate threat score
# 4. Trigger automated response
python main_ai_pipeline.py
```

The main pipeline uses pre-simulated data, but you can modify it to consume live monitoring data from the file monitor.

---

**Status**: ✅ Complete
**Last Updated**: March 6, 2026
**Owner**: Karan (Monitoring & Simulation)
