# Quick Start Guide 🚀

## Choose Your Tool

### 🐍 Python Script (Recommended)
**Best for**: Interactive use, detailed analysis, multiple test runs

```bash
sudo python3 usb_test.py
```

### 📜 Bash Script (Legacy)
**Best for**: Quick tests, shell scripting, minimal dependencies

```bash
sudo ./usb_test.sh -s /media/usb
```

---

## Installation (First Time Setup)

### Step 1: Install Dependencies

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install fio f3 python3
```

**Fedora/RHEL:**
```bash
sudo dnf install fio f3 python3
```

**Arch Linux:**
```bash
sudo pacman -S fio f3 python
```

### Step 2: Make Scripts Executable

```bash
cd /path/to/usb_tools
chmod +x usb_test.sh usb_test.py
```

### Step 3: Find Your USB Mount Point

```bash
lsblk
# or
df -h | grep media
```

Look for your USB drive (usually `/media/username/drivename` or `/mnt/usb`)

---

## Common Tasks

### 🎯 Test a New USB Drive (Full Validation)

**Python (Interactive):**
```bash
sudo python3 usb_test.py
# Select option 3 (Run All Tests)
```

**Python (Command Line):**
```bash
sudo python3 usb_test.py -a /media/usb
```

**Bash:**
```bash
sudo ./usb_test.sh -a /media/usb
```

⚠️ **Warning**: Capacity test will erase all data!

---

### ⚡ Quick Speed Test

**Python (5 iterations with stats):**
```bash
sudo python3 usb_test.py -s /media/usb
```

**Python (3 iterations - faster):**
```bash
sudo python3 usb_test.py -s /media/usb -n 3
```

**Bash (single test):**
```bash
sudo ./usb_test.sh -s /media/usb
```

---

### 📦 Check Drive Capacity

#### 🛡️ Non-Destructive (Safe - Keeps Your Files)

**Python:**
```bash
sudo python3 usb_test.py --safe /media/usb
```

**Bash:**
```bash
sudo ./usb_test.sh -p /media/usb
```

✅ **Safe**: Only tests free space, existing files are NOT touched!

#### 📦 Full Capacity Test (Destructive - Erases Data)

**Python:**
```bash
sudo python3 usb_test.py -c /media/usb
```

**Bash:**
```bash
sudo ./usb_test.sh -c /media/usb
```

⚠️ **Warning**: Erases ALL data! Backup first!
⏱️ **Time Required**: Several hours for large drives!

---

## Output Examples

### Python Speed Test Results
```
📊 Speed Test Results
───────────────────────────────────────────────

📖 READ PERFORMANCE:
  Average: 145.67 MB/s
  Maximum: 152.34 MB/s
  Minimum: 141.23 MB/s

✍️  WRITE PERFORMANCE:
  Average: 98.45 MB/s
  Maximum: 102.11 MB/s
  Minimum: 95.78 MB/s

🔌 USB VERSION ESTIMATE:
  🚀 USB 3.0 / 3.1 Gen 1

⭐ PERFORMANCE RATING:
  👍 Good performance
```

### Bash Speed Test Results
```
>>> RUNNING SPEED TEST <<<
---------------------------------------
  Read Speed  : 145.23 MiB/s
  Write Speed : 98.67 MiB/s
---------------------------------------
```

---

## Troubleshooting

### ❌ "Permission denied"
**Fix**: Use `sudo`
```bash
sudo python3 usb_test.py
```

### ❌ "command not found: fio"
**Fix**: Install dependencies
```bash
sudo apt install fio f3  # Ubuntu/Debian
sudo dnf install fio f3  # Fedora/RHEL
```

### ❌ "Mount point does not exist"
**Fix**: Find correct mount point
```bash
lsblk
df -h
mount | grep /media
```

### ❌ Python script won't run
**Fix**: Make it executable
```bash
chmod +x usb_test.py
```

Or run directly:
```bash
python3 usb_test.py
```

---

## When to Use Each Tool

### Use Python Script When:
- ✅ You want detailed statistics and analysis
- ✅ You need multiple test iterations
- ✅ You prefer an interactive menu
- ✅ You want USB version detection
- ✅ You like colorful, emoji-rich output
- ✅ You want to see consistency across tests

### Use Bash Script When:
- ✅ You need a quick single test
- ✅ You're writing shell scripts/automation
- ✅ You prefer minimal dependencies
- ✅ You're on a very minimal Linux install
- ✅ You want fastest execution (one test)

---

## Recommended Workflow

### For New USB Drives:
1. **Speed Test First** (Python with 5 iterations)
   ```bash
   sudo python3 usb_test.py -s /media/usb -n 5
   ```
2. **Analyze Results** - Check if speeds match specifications
3. **Capacity Test** (if speed test looks suspicious)
   ```bash
   sudo python3 usb_test.py -c /media/usb
   ```

### For Regular Testing:
1. Run quick speed test (Python 3 iterations or Bash)
   ```bash
   sudo python3 usb_test.py -s /media/usb -n 3
   # or
   sudo ./usb_test.sh -s /media/usb
   ```

---

## Performance Reference

| USB Standard | Theoretical Max | Realistic Speed |
|--------------|----------------|-----------------|
| USB 2.0 | 60 MB/s | 30-40 MB/s |
| USB 3.0 (3.1 Gen 1) | 625 MB/s | 100-400 MB/s |
| USB 3.1 Gen 2 | 1,250 MB/s | 500-900 MB/s |
| USB 3.2 Gen 2×2 | 2,500 MB/s | 1,000-2,000 MB/s |

---

## Safety Checklist

Before running capacity tests:

- [ ] Backup all important data
- [ ] Verify correct mount point
- [ ] Ensure you have time (can take hours)
- [ ] Understand test will erase all data
- [ ] Drive is not your system drive!

---

## Next Steps

- 📖 Read [USB_Test_PYTHON.md](USB_Test_PYTHON.md) for detailed Python documentation
- 📖 Read [USB_Test_BASH.md](USB_Test_BASH.md) for detailed Bash documentation
- 📖 Check [README.md](README.md) for feature comparison

---

## Quick Command Reference

### Python
```bash
# Interactive mode
sudo python3 usb_test.py

# Speed test (5 iterations)
sudo python3 usb_test.py -s /media/usb

# Speed test (custom iterations)
sudo python3 usb_test.py -s /media/usb -n 8

# Non-destructive capacity test (SAFE)
sudo python3 usb_test.py --safe /media/usb

# Full capacity test (DESTRUCTIVE)
sudo python3 usb_test.py -c /media/usb

# All tests (speed + full capacity)
sudo python3 usb_test.py -a /media/usb
```

### Bash
```bash
# Speed test only
sudo ./usb_test.sh -s /media/usb

# Non-destructive capacity test (SAFE)
sudo ./usb_test.sh -p /media/usb

# Full capacity test (DESTRUCTIVE)
sudo ./usb_test.sh -c /media/usb

# All tests (speed + full capacity)
sudo ./usb_test.sh -a /media/usb
```

---

**Happy Testing!** 💾✨
