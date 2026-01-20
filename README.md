# USB Tools 💾

Comprehensive USB drive testing utilities for Linux systems. Test drive speed and validate capacity to detect fake/counterfeit USB drives.

## 📦 Available Tools

### 1. **test_usb.py** - Cross-Platform Testing Suite ⭐ NEW!
**Universal USB tester - works everywhere!**
- 🌍 **Cross-platform**: Windows, macOS, and Linux
- 🎒 **Portable**: No dependencies, pure Python
- 📦 **Self-contained**: Single file, no installation
- 🎨 Interactive menu system
- 📊 Speed tests with statistics
- 🔐 Capacity tests with SHA-256 verification
- 🌈 Beautiful Unicode/emoji output
- ✅ Preserves existing files

**Best for**: Any platform, users without admin rights, portable testing

### 2. **usb_test.py** - Linux Testing Suite (Advanced)
Modern Python-based USB testing tool for Linux:
- 🎨 Interactive menu system
- 📊 Multiple speed test iterations with statistics
- 🛡️ Quick capacity test option (5 GB, ~10-20 min)
- 📦 Full capacity test with f3write/f3read
- ✅ Preserves existing files on your drive
- 🌈 Beautiful Unicode/emoji output
- 📈 Advanced performance analysis
- ⚡ Uses fio and f3 for thorough testing

**Best for**: Linux users, maximum testing capability

### 3. **usb_test.sh** - Bash Script (Legacy)
Original bash script for quick testing:
- Simple command-line interface
- Fast single-pass speed tests
- Full capacity testing with f3write/f3read
- Preserves existing files
- Capacity validation and fake drive detection

**Best for**: Shell scripting, minimalist approach

## 🚀 Quick Start

### Cross-Platform Version (Works Everywhere! ⭐)

**No installation, no dependencies, works on all platforms!**

**⚠️ REQUIRES: sudo (Linux/macOS) or Administrator (Windows)**

```bash
# Interactive mode (recommended)
sudo python3 test_usb.py               # Linux/macOS (REQUIRES sudo)
python test_usb.py                     # Windows (Run as Administrator)

# Command-line mode
python3 test_usb.py -s /media/usb      # Linux
python3 test_usb.py -s /Volumes/USB    # macOS
python test_usb.py -s E:\              # Windows

# All tests
python3 test_usb.py -a /media/usb      # Linux
python3 test_usb.py -a /Volumes/USB    # macOS
python test_usb.py -a E:\              # Windows
```

### Linux Testing Suite (Advanced)

**Requires fio and f3 tools installed:**

```bash
# Interactive mode
sudo python3 usb_test.py

# Speed test only
sudo python3 usb_test.py -s /media/usb

# Quick capacity test (5 GB, ~10-20 min)
sudo python3 usb_test.py -q /media/usb

# Full capacity test (all free space, hours)
sudo python3 usb_test.py -c /media/usb

# All tests (speed + full capacity)
sudo python3 usb_test.py -a /media/usb

# Custom iterations
sudo python3 usb_test.py -s /media/usb -n 8
```

### Bash Script

**Requires fio and f3 tools installed:**

```bash
# Speed test only
sudo ./usb_test.sh -s /media/usb

# Capacity test (fills all free space, preserves files)
sudo ./usb_test.sh -c /media/usb

# All tests (speed + capacity)
sudo ./usb_test.sh -a /media/usb
```

## 📋 System Requirements

### For test_usb.py (Cross-Platform)
- **Python 3.6+** - Usually pre-installed on modern systems
- **No other dependencies!** - Everything built-in

### For usb_test.py and usb_test.sh (Linux Only)
- **Python 3.6+** - Usually pre-installed
- **fio** - Flexible I/O Tester
- **f3** - Fight Flash Fraud tools

### Installation

**Fedora/RHEL/CentOS:**
```bash
sudo dnf install fio f3 python3
```

**Ubuntu/Debian:**
```bash
sudo apt install fio f3 python3
```

**Arch Linux:**
```bash
sudo pacman -S fio f3 python
```

## 📚 Documentation

- [**TEST_USB_CROSSPLATFORM.md**](TEST_USB_CROSSPLATFORM.md) - Cross-platform script guide ⭐ NEW!
- [**USB_Test_PYTHON.md**](USB_Test_PYTHON.md) - Linux Python script guide
- [**USB_Test_BASH.md**](USB_Test_BASH.md) - Bash script documentation
- [**CAPACITY_TESTING.md**](CAPACITY_TESTING.md) - Understanding capacity tests
- [**QUICK_START.md**](QUICK_START.md) - Quick reference guide

## ⚡ Features Comparison

| Feature | test_usb.py<br>(Cross-Platform) | usb_test.py<br>(Linux) | usb_test.sh<br>(Bash) |
|---------|--------------------------|-----------------|---------------|
| **Platform Support** | ⭐ Win/Mac/Linux | Linux only | Linux only |
| **Dependencies** | ⭐ None! | fio, f3 | fio, f3 |
| **Portability** | ⭐ Single file | Requires tools | Requires tools |
| Interactive Menu | ✅ | ✅ | ❌ |
| Multiple Test Iterations | ✅ | ✅ | ❌ |
| Statistics (avg/min/max) | ✅ | ✅ | ❌ |
| Unicode/Emoji Output | ✅ | ✅ | ❌ |
| USB Version Detection | ✅ | ✅ | ❌ |
| Performance Rating | ✅ | ✅ | ❌ |
| Colored Output | ✅ | ✅ | ❌ |
| Progress Indicators | ✅ | ✅ | ❌ |
| Command-line Mode | ✅ | ✅ | ✅ |
| Speed Test | ✅ Built-in | ✅ fio | ✅ fio |
| Quick Capacity Test | ✅ Adjustable | ✅ Python | ❌ |
| Full Capacity Test | ✅ Built-in | ✅ f3 | ✅ f3 |
| Data Verification | ✅ SHA-256 | ✅ f3 patterns | ✅ f3 patterns |
| Preserves Existing Files | ✅ | ✅ | ✅ |

## 🎯 Use Cases

- **Verify new USB drives** - Detect counterfeit/fake capacity drives
- **Performance testing** - Measure actual read/write speeds
- **Quality assurance** - Test drive reliability over multiple runs
- **Troubleshooting** - Identify slow or failing drives
- **Purchase validation** - Verify advertised specifications

## ⚠️ Important Notes

### test_usb.py (Cross-Platform) ⭐
- ✅ **No dependencies** - works on any system with Python
- ⚠️ **REQUIRES sudo/Administrator** - mandatory for accurate testing
- ✅ **Portable** - single file, copy and run anywhere
- ✅ **Safe** - preserves existing files, only uses free space
- ⏱️ **Accurate** - proper cache clearing and disk synchronization

### usb_test.py & usb_test.sh (Linux)
- **Root required**: Requires sudo/root privileges for direct I/O
- **Dependencies needed**: fio and f3 must be installed
- **Capacity tests preserve files**: Tests fill free space but do NOT delete existing files
- **Python offers two modes**:
  - 🛡️ **Quick test** (`-q`): Tests limited data, fast (~10-20 min)
  - 📦 **Full test** (`-c`): Tests all free space, thorough (hours)
- **Bash has one mode**: Full capacity test using f3write/f3read
- **Time required**: Full tests take hours on large drives

## 🤝 Contributing

Feel free to submit issues or pull requests for improvements!

## 📄 License

These tools are provided as-is for USB drive testing and validation purposes.
