# Changelog

## Version 2.0 - Non-Destructive Testing Support (January 2026)

### 🎉 Major New Feature: Non-Destructive Capacity Testing

Both the Python and Bash scripts now support **non-destructive capacity testing** using `f3probe`. This allows you to test your USB drive's capacity without erasing your existing files!

### What's New

#### 🛡️ Non-Destructive Capacity Test
- **Python**: `sudo python3 usb_test.py --safe /media/usb`
- **Bash**: `sudo ./usb_test.sh -p /media/usb`

**Benefits**:
- ✅ Tests free space without touching existing files
- ⚡ Faster than full capacity test
- 🔍 Detects obvious capacity fraud
- 💾 Safe for drives with important data

**How it works**:
- Uses `f3probe` to test only unallocated space
- Verifies the integrity of free space
- Reports any capacity anomalies
- Cleans up automatically

#### 📦 Full Capacity Test (Existing, Now Clearly Labeled)
- **Python**: `sudo python3 usb_test.py -c /media/usb`
- **Bash**: `sudo ./usb_test.sh -c /media/usb`

**Characteristics**:
- ⚠️ **DESTRUCTIVE** - Erases all data
- 🔍 Most thorough testing
- ⏱️ Takes hours on large drives
- 🛡️ Best for new/suspicious drives

### Enhanced Features

#### Python Script (`usb_test.py`)
1. **Updated Interactive Menu**:
   - Option 2: Non-destructive capacity test
   - Option 3: Full capacity test (destructive)
   - Option 4: All tests (speed + full capacity)
   - Option 5: Advanced speed test

2. **New Command-Line Options**:
   - `--safe` or `--capacity-safe`: Non-destructive test
   - `-c` or `--capacity`: Full destructive test
   - Clear labeling in help text

3. **Improved Dependency Checking**:
   - Detects if `f3probe` is available
   - Gracefully handles missing `f3probe`
   - Provides installation instructions

4. **Enhanced User Experience**:
   - 🛡️ Shield emoji for non-destructive tests
   - 🔍 Magnify emoji for probing operations
   - Clear warnings and confirmations
   - Detailed output explanations

#### Bash Script (`usb_test.sh`)
1. **New Option**:
   - `-p`: Non-destructive capacity test

2. **Smart Detection**:
   - Checks for `f3probe` availability
   - Provides fallback to destructive test
   - Clear error messages if `f3probe` missing

3. **Maintained Compatibility**:
   - All existing options still work
   - Same behavior for speed tests
   - Full capacity test unchanged

### Documentation Updates

All documentation has been updated to reflect the new features:

1. **USB_Test_BASH.md**:
   - New section: "Capacity Testing: Destructive vs Non-Destructive"
   - Updated command options table
   - New examples for both test types
   - Clear warnings and recommendations

2. **USB_Test_PYTHON.md**:
   - Comprehensive comparison of both test methods
   - Updated menu options
   - New examples with both approaches
   - Enhanced emoji legend

3. **QUICK_START.md**:
   - Quick reference for both test types
   - Side-by-side comparisons
   - Updated command reference
   - Safety highlights

4. **README.md**:
   - Updated feature highlights
   - Enhanced features comparison table
   - New quick start examples
   - Revised important notes section

### System Requirements

#### New Dependency (Optional)
- **f3probe**: Part of the f3 package (Fight Flash Fraud)
  - Required for non-destructive testing
  - Optional - scripts work without it
  - Full capacity test still available as fallback

#### Installation
```bash
# Ubuntu/Debian
sudo apt install f3

# Fedora/RHEL
sudo dnf install f3

# Arch Linux
sudo pacman -S f3
```

**Note**: Newer versions of the f3 package include `f3probe`. Older versions may only have `f3write` and `f3read`.

### Use Cases

#### Use Non-Destructive Test When:
- ✅ Drive already has files you want to keep
- ✅ Quick capacity verification needed
- ✅ Regular drive health checks
- ✅ Testing drives in active use
- ✅ Don't have time for hours-long tests

#### Use Full Capacity Test When:
- ✅ Testing brand new USB drives
- ✅ Suspected counterfeit/fake drives
- ✅ Most thorough validation needed
- ✅ Pre-deployment validation
- ✅ After backing up all data

### Breaking Changes

**None!** All existing commands and options continue to work exactly as before.

### Migration Guide

#### If You Were Using:
```bash
# Old way (still works)
sudo python3 usb_test.py -c /media/usb
```

#### You Can Now Also Use:
```bash
# New non-destructive option
sudo python3 usb_test.py --safe /media/usb
```

### Performance

#### Non-Destructive Test:
- ⚡ **Duration**: Minutes to ~30 minutes
- 💾 **Disk Usage**: Only tests free space
- 🔍 **Coverage**: Free space only

#### Full Capacity Test:
- ⏱️ **Duration**: Hours on large drives
- 💾 **Disk Usage**: Fills entire drive
- 🔍 **Coverage**: Complete drive

### Known Limitations

1. **f3probe Availability**:
   - Not included in older f3 packages
   - May need to update f3 package
   - Scripts detect and handle gracefully

2. **Non-Destructive Test Coverage**:
   - Only tests unallocated space
   - May miss issues in used areas
   - Less comprehensive than full test

3. **Platform Support**:
   - Linux only (both test types)
   - Requires root/sudo privileges

### Future Enhancements

Potential future additions:
- [ ] Progress bars for long operations
- [ ] Test result logging to file
- [ ] Benchmark database comparison
- [ ] Email notifications on completion
- [ ] GUI version
- [ ] MacOS/Windows support via alternative tools

### Contributors

Enhancement implemented in response to user request for safer testing options.

### Feedback

If you encounter issues with the non-destructive testing feature:
1. Verify `f3probe` is installed: `which f3probe`
2. Check f3 package version: `f3probe --version`
3. Update f3 if needed: `sudo apt update && sudo apt upgrade f3`
4. Fall back to full capacity test if needed

---

## Version 1.0 - Initial Release (January 2026)

### Initial Features

#### Python Script
- Interactive menu system
- Multiple speed test iterations
- Statistical analysis
- Unicode/emoji output
- USB version detection
- Performance ratings
- Command-line mode

#### Bash Script  
- Speed testing with fio
- Capacity testing with f3
- Simple command-line interface
- Single-pass testing

#### Documentation
- Comprehensive guides for both scripts
- Quick start guide
- Installation instructions
- Troubleshooting tips

---

**Current Version**: 2.0
**Last Updated**: January 17, 2026
