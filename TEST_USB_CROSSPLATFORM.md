# Cross-Platform USB Testing Suite 💾

## Overview

`test_usb.py` is a **completely portable**, cross-platform USB testing tool that works on **Windows, macOS, and Linux** without any external dependencies. Everything is built-in using only Python's standard library!

### 🆕 Latest Features (v1.1)

- ⚡ **High-Performance Mode**: 2GB test files for accurate testing of fast drives (1000+ MB/s)
- 📦 **Full Capacity Testing**: Test ALL free space to detect fake drives
- 🛡️ **Quick Capacity Test**: Fast 5GB verification for trusted drives
- 📊 **Improved Cache Handling**: Better accuracy on Linux with sudo
- 🎯 **Smart Test Size Recommendations**: Automatic guidance for optimal test sizes
- 📈 **Enhanced Statistics**: Better consistency detection via standard deviation

## ✨ Key Features

### 🌍 Cross-Platform
- ✅ **Windows** (7, 8, 10, 11)
- ✅ **macOS** (10.12+)
- ✅ **Linux** (all distributions)

### 🎒 Portable
- ✅ **No external dependencies** (no fio, no f3)
- ✅ **Pure Python** implementation
- ✅ **Single file** - easy to copy and run anywhere
- ✅ **Requires only Python 3.6+** (usually pre-installed)

### 🎨 User-Friendly
- ✅ Interactive menu system
- ✅ Beautiful emoji and color output
- ✅ Progress indicators
- ✅ Command-line mode for scripting
- ✅ Platform-specific path guidance

### 🛡️ Safe
- ✅ Preserves existing files
- ✅ Only uses free space
- ✅ Automatic cleanup
- ✅ Can interrupt safely (Ctrl+C)

## 🚀 Quick Start

### Installation

No installation needed! Just have Python 3.6+ installed:

**Check Python version:**
```bash
python3 --version
# or on Windows:
python --version
```

**Download the script** (or copy it to your system)

## 📖 Complete Usage Guide

### Step-by-Step: Testing Your First USB Drive

**Step 1: Find Your USB Drive Path**

**Windows:**
```cmd
# Open Command Prompt and type:
wmic logicaldisk get name
# Look for your USB drive letter (e.g., E:, F:, G:)
```

**macOS:**
```bash
ls /Volumes/
# Your USB will be listed (e.g., /Volumes/MyUSB)
```

**Linux:**
```bash
lsblk
# or
df -h | grep media
# Look for /media/username/USB_DRIVE
```

**Step 2: Run Interactive Mode**
```bash
# Linux/macOS (use sudo for best results)
sudo python3 test_usb.py

# Windows (run as Administrator for best results)  
python test_usb.py
```

**Step 3: Choose Your Test from the Menu**

The menu will show:
```
1. ⚡ Speed Test - Standard (5x 512MB)
2. 🔥 Speed Test - High Performance (5x 2GB)
3. 🛡️  Capacity Test - Quick (5 GB)
4. 📦 Capacity Test - Full (All Free Space)
5. 🚀 Run All Tests
6/7. Custom options
```

### Common Testing Scenarios

#### 📦 New USB Drive from Store
**Goal**: Verify it's genuine and performs as advertised

```bash
sudo python3 test_usb.py

# Menu choices:
# 1. Select Option 2 (High Performance) or 1 (Standard) based on drive speed
# 2. Review speed results
# 3. Select Option 4 (Full Capacity Test) - tests entire drive
# 4. Wait for completion (may take hours for large drives)
```

**What you're checking:**
- ✅ Speeds match specifications
- ✅ Full capacity is real (not fake)
- ✅ No data corruption

#### 🔍 Suspected Fake Drive
**Goal**: Prove if capacity is fraudulent

```bash
# Direct command for full capacity test
sudo python3 test_usb.py -c /media/usb --full-capacity

# For a fake "256GB" that's really 32GB:
# Result: Files beyond 32GB will show as CORRUPTED
```

#### ⚡ Fast Drive (1000+ MB/s)
**Goal**: Accurate measurement of high-speed drives

```bash
# Use high-performance mode with large test files
sudo python3 test_usb.py -s /media/usb --fast

# Or even larger for ultra-fast drives
sudo python3 test_usb.py -s /media/usb --size-mb 4096 -n 5
```

**Why?** 512MB on a 1000MB/s drive = 0.5 seconds (too fast!)
2GB on a 1000MB/s drive = 2 seconds (accurate!)

#### 🏥 Health Check
**Goal**: Quick verification drive is working

```bash
# Quick 15-minute check
python3 test_usb.py -s /media/usb          # Speed test
python3 test_usb.py -c /media/usb --size-gb 5  # Quick capacity
```

### Usage

#### Interactive Mode (Recommended)

```bash
# Linux/macOS
python3 test_usb.py

# Windows
python test_usb.py
```

#### Command-Line Mode

**Linux:**
```bash
python3 test_usb.py -s /media/usb                 # Standard (512MB)
python3 test_usb.py -s /media/usb --fast          # High-performance (2GB)
python3 test_usb.py -s /media/usb --size-mb 4096  # Custom (4GB)
python3 test_usb.py -c /mnt/usb --size-gb 10
python3 test_usb.py -a /media/usb
```

**macOS:**
```bash
python3 test_usb.py -s /Volumes/MyUSB
python3 test_usb.py -s /Volumes/MyUSB --fast      # For fast drives
python3 test_usb.py -a /Volumes/MyUSB
```

**Windows:**
```cmd
python test_usb.py -s E:\
python test_usb.py -s E:\ --fast                  # For fast drives
python test_usb.py -c F:\ --size-gb 10
python test_usb.py -a G:\
```

## 📋 Menu Options

### Interactive Menu
```
1. ⚡ Speed Test - Standard (5x 512MB)
2. 🔥 Speed Test - High Performance (5x 2GB)
3. 🛡️  Capacity Test - Quick (5 GB)
4. 📦 Capacity Test - Full (All Free Space)
5. 🚀 Run All Tests (Standard + Full Capacity)
6. ⚙️  Custom Speed Test
7. ⚙️  Custom Capacity Test
0. ❌ Exit

Tip: Full capacity test fills entire drive - best for detecting fake drives
```

### Choosing the Right Test Size

| Drive Type | Expected Speed | Recommended Test Size | Mode |
|------------|---------------|----------------------|------|
| USB 2.0 | 20-40 MB/s | 512 MB | Standard |
| USB 3.0 | 100-400 MB/s | 512 MB | Standard |
| USB 3.1/3.2 | 500-1000 MB/s | 2 GB | High Performance |
| NVMe/Thunderbolt | 1000-3000 MB/s | 2-4 GB | High Performance |
| Ultra-fast NVMe | >3000 MB/s | 4-8 GB | Custom |

**Why larger files for fast drives?**
- **Timing accuracy**: 512MB on a 1000MB/s drive = 0.5 seconds (too fast!)
- **Cache effects**: Larger files less likely to fit in cache
- **Realistic testing**: Larger files better represent real-world usage
- **Consistent results**: More data = more accurate statistics

## 🔬 How It Works - Technical Deep Dive

### Overview

`test_usb.py` is a pure Python implementation that uses only the standard library. No external tools (like fio or f3) are required. This makes it truly portable across all platforms.

### Speed Testing Technology

**What it does:**
1. Generates test data with known patterns
2. Writes data to disk with fsync() to ensure real disk writes
3. Reads data back
4. Measures actual throughput
5. Repeats multiple times for accuracy
6. Calculates statistics (avg, min, max, std dev)

**Default Settings:**
- **Iterations**: 5
- **Test Size**: 512 MB per iteration (Standard mode)
- **Test Size**: 2048 MB per iteration (High Performance mode)
- **Total Data**: ~2.5 GB (Standard) or ~10 GB (High Performance)

**What you get:**
- Read/Write speeds in MB/s
- Statistical analysis (avg, min, max, std dev)
- USB version estimate
- Performance rating
- Test size recommendations
- Cache warnings (Linux without sudo)

### Capacity Testing

**Pure Python implementation with checksum verification!**

**What it does:**
1. Creates test files in free space
2. Generates data with SHA-256 checksums
3. Writes test files (100 MB each)
4. Verifies each file:
   - File exists
   - Size is correct
   - Checksum matches (data integrity)
5. Reports any errors
6. Cleans up automatically

**Default Settings:**
- **Test Size**: 5 GB
- **File Size**: 100 MB per file
- **Verification**: Full checksum validation

**What you get:**
- Data integrity verification
- Corruption detection
- Fake drive detection
- Read/Write speeds during test

## 💻 Platform-Specific Usage

### Windows

**Path Format:**
```cmd
E:\
F:\Users\Data
G:\
```

**Running:**
```cmd
# Interactive
python test_usb.py

# Speed test on E: drive
python test_usb.py -s E:\

# Capacity test on F: drive
python test_usb.py -c F:\ --size-gb 10

# All tests
python test_usb.py -a G:\
```

**Notes:**
- ANSI colors enabled automatically
- Drive letters (C:, D:, E:, etc.)
- Administrator rights may be needed for some drives

### macOS

**Path Format:**
```bash
/Volumes/USB_DRIVE
/Volumes/MyDrive
```

**Running:**
```bash
# Interactive
python3 test_usb.py

# Speed test
python3 test_usb.py -s /Volumes/USB_DRIVE

# Capacity test
python3 test_usb.py -c /Volumes/MyDrive --size-gb 10

# All tests
python3 test_usb.py -a /Volumes/USB_DRIVE
```

**Notes:**
- Usually located in `/Volumes/`
- May need sudo for some operations
- Full Unicode/emoji support

### Linux

**Path Format:**
```bash
/media/username/USB_DRIVE
/mnt/usb
/run/media/username/drive
```

**Running:**
```bash
# Interactive
python3 test_usb.py

# Speed test
python3 test_usb.py -s /media/usb

# Capacity test
python3 test_usb.py -c /mnt/usb --size-gb 10

# All tests
python3 test_usb.py -a /media/usb
```

**Notes:**
- Common mount points: `/media/`, `/mnt/`, `/run/media/`
- May need sudo for some operations
- Full Unicode/emoji support

## 📊 Understanding Results

### Speed Test Output

```
📊 Speed Test Results
───────────────────────────────────────────────

📖 READ PERFORMANCE:
  Average: 145.67 MB/s
  Maximum: 152.34 MB/s
  Minimum: 141.23 MB/s
  Std Dev: 3.89 MB/s

✍️  WRITE PERFORMANCE:
  Average: 98.45 MB/s
  Maximum: 102.11 MB/s
  Minimum: 95.78 MB/s
  Std Dev: 2.34 MB/s

🔌 USB VERSION ESTIMATE:
  🚀 USB 3.0 / 3.1 Gen 1

⭐ PERFORMANCE RATING:
  👍 Good performance
```

### Capacity Test Output

```
📦 Capacity Test Results
───────────────────────────────────────────────

✅ ALL TESTS PASSED!
ℹ️  Tested 5 GB successfully
ℹ️  No data corruption detected
ℹ️  Drive capacity appears genuine
```

**Or if there are issues:**
```
❌ 5 ERROR(S) DETECTED!
⚠️  Drive may have capacity issues or be counterfeit
⚠️  Some data was corrupted or lost
```

## ⚙️ Command-Line Options

### Basic Options

| Option | Description |
|--------|-------------|
| `path` | USB drive path (required for CLI mode) |
| `-s, --speed` | Run speed test only |
| `-c, --capacity` | Run capacity test only |
| `-a, --all` | Run all tests |
| `-h, --help` | Show help message |

### Advanced Options

| Option | Description | Default |
|--------|-------------|---------|
| `-n, --iterations` | Number of speed test iterations | 5 |
| `--fast` | High-performance mode (2GB test files) | Off |
| `--full-capacity` | Test ALL free space (best fake detection) | Off |
| `--size-mb` | Speed test size in MB | 512 (2048 with --fast) |
| `--size-gb` | Capacity test size in GB | 5 |
| `--no-interactive` | Disable interactive mode | False |

### Examples

**Custom speed test (8 iterations, 512MB):**
```bash
python3 test_usb.py -s /media/usb -n 8 --size-mb 512
```

**Large capacity test (20GB):**
```bash
python3 test_usb.py -c /media/usb --size-gb 20
```

**Quick all tests (3 iterations, 2GB capacity):**
```bash
python3 test_usb.py -a /media/usb -n 3 --size-gb 2
```

## 🔧 Technology & Algorithms Explained

### Speed Test Algorithm - Deep Dive

#### Write Test Implementation

**Complete Algorithm:**
```python
def run_write_test(path, size_mb):
    """Accurate write speed measurement"""
    test_file = path / f'speed_test_{timestamp}.tmp'
    
    # Step 1: Generate test data (memory-efficient generator)
    def generate_test_data(size_mb):
        pattern = b'USB_TEST_' + os.urandom(54)  # 64-byte pattern
        chunk_1mb = pattern * (1024*1024 // 64)  # Repeat to 1MB
        for _ in range(size_mb):
            yield chunk_1mb
    
    start_time = time.time()
    
    # Step 2: Write with unbuffered I/O
    with open(test_file, 'wb', buffering=0) as f:  # NO BUFFERING!
        for chunk in generate_test_data(size_mb):
            f.write(chunk)
            # Periodic fsync every 10MB
            if bytes_written % (10 * 1024 * 1024) == 0:
                os.fsync(f.fileno())  # Force to disk
        
        # Final sync to ensure everything is written
        os.fsync(f.fileno())
    
    duration = time.time() - start_time
    speed_mb_s = size_mb / duration
    return speed_mb_s
```

**Why This Works:**
1. `buffering=0` - Bypasses Python's internal buffer
2. `os.fsync()` - Forces kernel to write to physical device
3. `os.urandom()` - Creates incompressible random data
4. Generator - Memory efficient (can test 4GB without 4GB RAM)

#### Read Test Implementation

**Complete Algorithm:**
```python
def run_read_test(test_file, size_mb):
    """Accurate read speed measurement with cache handling"""
    
    # Step 1: Clear OS cache (Linux only, requires sudo)
    def clear_cache():
        if platform.system() == 'Linux':
            try:
                # Drop PageCache, dentries, and inodes
                with open('/proc/sys/vm/drop_caches', 'w') as f:
                    f.write('3\n')
            except PermissionError:
                os.sync()  # Best effort without sudo
        else:
            os.sync()
    
    clear_cache()
    time.sleep(0.5)  # Let cache clear take effect
    
    start_time = time.time()
    bytes_read = 0
    
    # Step 2: Read with unbuffered I/O
    with open(test_file, 'rb', buffering=0) as f:
        while True:
            chunk = f.read(1024 * 1024)  # 1MB chunks
            if not chunk:
                break
            bytes_read += len(chunk)
            _ = len(chunk)  # Process data (prevent optimization)
    
    duration = time.time() - start_time
    speed_mb_s = size_mb / duration
    return speed_mb_s
```

**Cache Handling Deep Dive:**

**Linux `/proc/sys/vm/drop_caches` values:**
- `1` - Clear PageCache only
- `2` - Clear dentries and inodes
- `3` - Clear everything (what we use)

**The Cache Problem:**
```
Without cache clearing:
Test 1: 200 MB/s  (reads from USB)
Test 2: 4000 MB/s (reads from RAM cache!) ❌

With cache clearing:
Test 1: 185 MB/s  (reads from USB)
Test 2: 186 MB/s  (reads from USB) ✅
```

#### Statistical Analysis

**Standard Deviation Calculation:**
```python
from statistics import mean, stdev

speeds = [185, 186, 75, 190, 189]  # MB/s from 5 tests

avg = mean(speeds)  # 165.0 MB/s
std = stdev(speeds)  # 50.37 MB/s (high = inconsistent!)

# Interpretation:
if std < 5:
    print("Excellent consistency")
elif std < 15:
    print("Normal variation")
else:
    print("Inconsistent - check for issues")  # This case!
```

**USB Version Detection:**
```python
def detect_usb_version(read_speed, write_speed):
    max_speed = max(read_speed, write_speed)
    
    # Based on theoretical maximums
    if max_speed < 50:
        return "USB 2.0", 60        # Theoretical: 60 MB/s
    elif max_speed < 450:
        return "USB 3.0/3.1 Gen 1", 625   # Theoretical: 625 MB/s
    elif max_speed < 1000:
        return "USB 3.1 Gen 2", 1250      # Theoretical: 1250 MB/s
    else:
        return "USB 3.2+", 2500+          # Theoretical: 2500+ MB/s
```

### Capacity Test Algorithm - Deep Dive

#### SHA-256 Checksum Verification

**Why SHA-256?**
- Cryptographically secure (collision probability: 2^-256)
- Fast on modern CPUs
- Detects even single-bit corruption
- Standard library (no dependencies)

**Implementation:**
```python
import hashlib

def write_and_hash_file(filepath, size_mb):
    """Write file and calculate checksum"""
    hasher = hashlib.sha256()
    
    with open(filepath, 'wb') as f:
        for chunk in generate_test_data(size_mb):
            f.write(chunk)
            hasher.update(chunk)  # Hash as we write
    
    checksum = hasher.hexdigest()  # 64-char hex string
    return checksum

def verify_file(filepath, expected_checksum, expected_size):
    """Verify file integrity"""
    # Check 1: File exists
    if not filepath.exists():
        return "MISSING"
    
    # Check 2: Correct size
    actual_size = filepath.stat().st_size
    if actual_size != expected_size:
        return "SIZE_MISMATCH"
    
    # Check 3: Data integrity via checksum
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(1024 * 1024):
            hasher.update(chunk)
    
    if hasher.hexdigest() == expected_checksum:
        return "OK"
    else:
        return "CORRUPTED"
```

#### Fake Drive Detection Logic

**How Fake Drives Work:**
A fake "256GB" USB drive that's really 32GB:
```
Reported capacity: 256 GB
Actual capacity: 32 GB
Fake capacity: 224 GB
```

**What happens when you write:**
```
Bytes 0 - 32GB:   Written correctly ✅
Bytes 32GB - 64GB: Overwrites bytes 0-32GB ❌
Bytes 64GB - 96GB: Overwrites bytes 0-32GB again ❌
...and so on (wraps around)
```

**Our Test Detects This:**
```python
# Write Phase
files_written = 2560  # 256 GB ÷ 100 MB per file
checksums = {}

for i in range(files_written):
    path = f"test_{i:04d}.dat"
    checksum = write_file(path, 100)  # Write 100MB
    checksums[path] = checksum

# Read/Verify Phase
errors = 0
for path, expected_checksum in checksums.items():
    actual_checksum = read_and_hash_file(path)
    if actual_checksum != expected_checksum:
        errors += 1

# Results:
# Files 0-319: OK (32 GB of real capacity)
# Files 320-2559: CORRUPTED (wrapped around, overwritten)
# 
# Conclusion: Drive is FAKE!
```

#### Full vs Quick Capacity Test

**Quick Test (5 GB):**
```python
test_size_gb = 5
num_files = 50  # 5 GB ÷ 100 MB
time_estimate = 10  # minutes
```

**Pros:**
- Fast verification
- Detects obvious fakes
- Good for known drives

**Cons:**
- Won't detect fake "256GB" that's actually "64GB"
- Misses issues beyond tested area

**Full Test (All Free Space):**
```python
free_space_gb = get_free_space()
test_size_gb = free_space_gb - 0.5  # Leave 500MB buffer
num_files = test_size_gb * 10  # 10 files per GB
time_estimate = test_size_gb * 2  # ~2 min per GB
```

**Pros:**
- Tests entire drive
- Detects all fake capacity
- Finds bad sectors anywhere
- Maximum confidence

**Cons:**
- Time consuming (hours for large drives)
- Temporarily fills drive

### Memory Efficiency

**Generator Pattern:**
```python
def generate_test_data(size_mb):
    """Memory-efficient data generation"""
    pattern = b'USB_TEST_' + os.urandom(54)
    chunk_1mb = pattern * (1024*1024 // 64)
    
    for _ in range(size_mb):
        yield chunk_1mb  # Generates on-demand

# Usage:
for chunk in generate_test_data(4096):  # 4GB test
    write(chunk)  # Only 1MB in memory at a time!
```

**vs. Loading Everything:**
```python
# BAD: Would need 4GB RAM!
data = b'x' * (4096 * 1024 * 1024)
write(data)
```

### Platform-Specific Optimizations

**Linux:**
- Direct cache control via `/proc/sys/vm/drop_caches`
- Most accurate results with sudo
- fsync() well-supported

**macOS:**
- No direct cache control API
- Relies on larger test files
- fcntl() with F_NOCACHE flag (future enhancement)

**Windows:**
- No direct cache control
- FILE_FLAG_NO_BUFFERING (future enhancement)
- ANSI color support via ctypes

### Performance Characteristics

**Time Complexity:**
- Write test: O(n) where n = test size
- Read test: O(n) where n = test size
- Capacity test: O(m*n) where m = files, n = file size

**Space Complexity:**
- Generator pattern: O(1) - constant memory
- Checksum storage: O(m) where m = number of files

**I/O Patterns:**
- Sequential writes (optimal for all storage)
- Sequential reads (optimal for all storage)
- Large block sizes (1MB) minimize overhead

### Why Not Random I/O?

**Sequential vs Random:**
```
Sequential (what we do):
- USB 3.0 SSD: 400 MB/s
- USB 3.0 HDD: 100 MB/s

Random (not tested):
- USB 3.0 SSD: 300 MB/s
- USB 3.0 HDD: 1 MB/s (terrible!)
```

**Reasons for Sequential:**
1. Represents common use cases (file copies)
2. Fair comparison across device types
3. More consistent results
4. Easier to understand for users

## 🔧 Technical Implementation Details

### Core Speed Test Code

```python
# Complete write test (simplified)
def run_write_test(path, size_mb):
    test_file = path / f'speed_test_{time.time()}.tmp'
    start = time.time()
    
    with open(test_file, 'wb', buffering=0) as f:
        for chunk in generate_test_data(size_mb):
            f.write(chunk)
            if bytes_written % (10*1024*1024) == 0:
                os.fsync(f.fileno())
        os.fsync(f.fileno())
    
    duration = time.time() - start
    return size_mb / duration, test_file
```

### Core Capacity Test Code

```python
# Complete capacity test (simplified)
def run_capacity_test(path, test_size_gb):
    test_dir = path / f'capacity_test_{time.time()}'
    test_dir.mkdir()
    
    file_size_mb = 100
    num_files = test_size_gb * 10
    checksums = {}
    
    # Write Phase
    for i in range(num_files):
        file_path = test_dir / f'test_{i:04d}.dat'
        hasher = hashlib.sha256()
        
        with open(file_path, 'wb') as f:
            for chunk in generate_test_data(file_size_mb):
                f.write(chunk)
                hasher.update(chunk)
        
        checksums[file_path.name] = hasher.hexdigest()
    
    # Verify Phase
    errors = 0
    for filename, expected_hash in checksums.items():
        file_path = test_dir / filename
        
        if not file_path.exists():
            errors += 1
            continue
        
        # Verify checksum
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while chunk := f.read(1024*1024):
                hasher.update(chunk)
        
        if hasher.hexdigest() != expected_hash:
            errors += 1
    
    # Cleanup
    shutil.rmtree(test_dir)
    
    return errors == 0
```

### Memory Efficiency

- Uses **generators** for test data (low memory usage)
- **Streaming** reads and writes
- **Chunked processing** (1MB chunks)
- Can test drives larger than RAM

### Test Data Pattern

- Generated using `os.urandom()` for randomness
- Includes markers for identification
- Different patterns for each iteration
- SHA-256 checksums for verification

## 🆚 Comparison with Other Scripts

| Feature | test_usb.py | usb_test.py | usb_test.sh |
|---------|-------------|-------------|-------------|
| **Cross-Platform** | ✅ Win/Mac/Linux | ❌ Linux only | ❌ Linux only |
| **No Dependencies** | ✅ Pure Python | ❌ Needs fio, f3 | ❌ Needs fio, f3 |
| **Portable** | ✅ Single file | ❌ Requires tools | ❌ Requires tools |
| **Interactive Menu** | ✅ | ✅ | ❌ |
| **Speed Stats** | ✅ | ✅ | ❌ |
| **Capacity Test** | ✅ Built-in | ✅ f3write/f3read | ✅ f3write/f3read |
| **Data Verification** | ✅ SHA-256 | ✅ f3 patterns | ✅ f3 patterns |
| **Quick Test Option** | ✅ Adjustable | ✅ | ❌ |

### When to Use Each

**Use test_usb.py when:**
- ✅ You need cross-platform support
- ✅ You can't install external tools
- ✅ You want a portable solution
- ✅ You're on Windows or macOS
- ✅ You want a self-contained tool

**Use usb_test.py when:**
- ✅ You're on Linux
- ✅ You have fio and f3 installed
- ✅ You want f3's proven algorithms
- ✅ You need the most thorough testing

**Use usb_test.sh when:**
- ✅ You prefer bash scripts
- ✅ You're on Linux
- ✅ You have fio and f3 installed
- ✅ You want simplest interface

## 🛠️ Troubleshooting

### "Path does not exist"
**Solution:** Check the path carefully
- **Windows**: `E:\` not `E:`
- **macOS**: `/Volumes/DriveName`
- **Linux**: Check `lsblk` or `df -h`

### "Path is not writable"
**Solution:** Check permissions
```bash
# Linux/macOS
sudo python3 test_usb.py

# Windows: Run Command Prompt as Administrator
```

### "Insufficient space"
**Solution:** Reduce test size
```bash
# Smaller speed test
python3 test_usb.py -s /media/usb --size-mb 100

# Smaller capacity test
python3 test_usb.py -c /media/usb --size-gb 2
```

### Colors not working (Windows)
**Solution:** 
- Use Windows 10 or later
- Use Windows Terminal or modern command prompt
- Colors automatically enabled if supported

### Slow performance
**Causes:**
- USB 2.0 drive (max ~40 MB/s)
- Slow drive
- USB hub
- Background processes

**Solutions:**
- Use direct USB port (no hub)
- Close other programs
- Use USB 3.0+ port

## 💡 Best Practices

### 1. Start with Interactive Mode
Get familiar with the tool before using command-line mode.

### 2. Test New Drives Immediately
Run capacity test on any new USB drive to verify it's genuine.

### 3. Regular Speed Checks
Periodically test drive performance to catch degradation early.

### 4. Use Appropriate Test Sizes
- **Quick check**: 256MB speed, 2GB capacity
- **Standard check**: 256MB speed, 5GB capacity
- **Thorough check**: 512MB speed, 10GB+ capacity

### 5. Multiple Iterations
Use 5-10 iterations for accurate speed measurements.

### 6. Check USB Port Version
Use USB 3.0+ ports for USB 3.0+ drives.

## 🔒 Security & Privacy

- ✅ **No network access** - completely offline
- ✅ **No data collection** - nothing sent anywhere
- ✅ **No existing files read** - only writes new test files
- ✅ **No installation** - runs directly
- ✅ **Open source** - you can review the code

## 📦 Distribution

### As Single File
Just copy `test_usb.py` - that's it!

```bash
# Copy to USB drive for testing other systems
cp test_usb.py /media/usb/

# Use on another system
python3 test_usb.py -s /media/other_usb
```

### Requirements
- Python 3.6 or higher
- Standard library only (no pip packages)

### Size
- ~20KB - tiny and portable!

## 🚀 Advanced Usage

### Automation

**Test multiple drives (Linux/macOS):**
```bash
for drive in /media/usb*; do
    echo "Testing $drive"
    python3 test_usb.py -s "$drive" -n 3
done
```

**Scheduled testing (cron):**
```bash
# Add to crontab
0 2 * * * python3 /path/to/test_usb.py -s /media/usb >> /var/log/usb_test.log
```

### Logging Results

```bash
# Redirect output to file
python3 test_usb.py -a /media/usb 2>&1 | tee usb_test_$(date +%Y%m%d).log
```

### CI/CD Integration

```yaml
# GitHub Actions example
- name: Test USB Drive
  run: python3 test_usb.py -s /mnt/test --size-mb 100
```

## 🐛 Known Limitations

1. **Not as fast as compiled tools** - Python is slower than C/C++
2. **Basic algorithms** - Not as sophisticated as f3's algorithms
3. **Requires Python** - Not a standalone binary
4. **Terminal-based** - No GUI (by design)

## 🎯 Future Enhancements

Potential additions:
- [ ] S.M.A.R.T. data reading
- [ ] Sequential vs random I/O testing
- [ ] Latency measurements
- [ ] Temperature monitoring (if available)
- [ ] HTML report generation
- [ ] GUI version

## 📄 License

Provided as-is for USB drive testing and validation purposes.

## 📋 Quick Reference Card

### Essential Commands

```bash
# Interactive mode (easiest)
sudo python3 test_usb.py

# Speed test (standard USB drives)
python3 test_usb.py -s /media/usb

# Speed test (fast drives >500 MB/s)
python3 test_usb.py -s /media/usb --fast

# Quick capacity check (5 GB)
python3 test_usb.py -c /media/usb --size-gb 5

# Full capacity test (detect fakes)
python3 test_usb.py -c /media/usb --full-capacity

# Complete test suite
python3 test_usb.py -a /media/usb
```

### When to Use Each Test

| Situation | Command | Time |
|-----------|---------|------|
| **Quick check** | `-s /media/usb` | 30 seconds |
| **Fast drive** | `-s /media/usb --fast` | 1 minute |
| **Verify works** | `-c /media/usb --size-gb 5` | 10 minutes |
| **Detect fakes** | `-c /media/usb --full-capacity` | Hours |
| **New drive** | `-a /media/usb` then full capacity | Hours |

### Technology Summary

**Speed Tests:**
- Pure Python with unbuffered I/O
- fsync() for accurate disk writes
- Cache clearing on Linux (with sudo)
- Multiple iterations for statistics
- 512MB (standard) or 2GB+ (fast drives)

**Capacity Tests:**
- SHA-256 checksum verification
- 100MB files for thorough coverage
- Detects fake capacity and corruption
- Tests 5GB (quick) or all space (full)
- Memory-efficient generators

---

**Version**: 1.1
**Last Updated**: January 18, 2026  
**Python Required**: 3.6+  
**Platforms**: Windows, macOS, Linux
