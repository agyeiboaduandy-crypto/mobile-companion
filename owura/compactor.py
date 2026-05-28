"""
OWURA Compaction System - Automatic cache cleanup and memory management
Keeps your phone running smooth during heavy operations.
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
import time

class Compactor:
    def __init__(self):
        self.home = Path.home()
        self.temp_dir = Path("/tmp") if Path("/tmp").exists() else self.home / ".owura" / "temp"
        self.log_file = self.home / ".owura" / "compaction.log"
    
    def log(self, message: str):
        """Log compaction actions."""
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a") as f:
            f.write(f"[{timestamp}] {message}\n")
    
    def get_disk_usage(self) -> dict:
        """Get disk usage stats."""
        try:
            stat = shutil.disk_usage("/")
            return {
                "total_gb": round(stat.total / (1024**3), 2),
                "used_gb": round(stat.used / (1024**3), 2),
                "free_gb": round(stat.free / (1024**3), 2),
                "percent_used": round((stat.used / stat.total) * 100, 1)
            }
        except:
            return {"total_gb": 0, "used_gb": 0, "free_gb": 0, "percent_used": 0}
    
    def get_memory_usage(self) -> dict:
        """Get memory usage stats."""
        try:
            with open("/proc/meminfo") as f:
                lines = f.readlines()
            
            mem_info = {}
            for line in lines:
                parts = line.split(":")
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip().split()[0]
                    mem_info[key] = int(value)
            
            total = mem_info.get("MemTotal", 0)
            available = mem_info.get("MemAvailable", 0)
            used = total - available
            
            return {
                "total_mb": round(total / 1024, 1),
                "used_mb": round(used / 1024, 1),
                "available_mb": round(available / 1024, 1),
                "percent_used": round((used / total) * 100, 1) if total > 0 else 0
            }
        except:
            return {"total_mb": 0, "used_mb": 0, "available_mb": 0, "percent_used": 0}
    
    def get_cache_sizes(self) -> dict:
        """Get sizes of common caches."""
        caches = {}
        
        # pip cache
        pip_cache = self.home / ".cache" / "pip"
        if pip_cache.exists():
            caches["pip"] = self._get_dir_size(pip_cache)
        
        # npm cache
        npm_cache = self.home / ".npm"
        if npm_cache.exists():
            caches["npm"] = self._get_dir_size(npm_cache)
        
        # Termux cache
        termux_cache = Path("/data/data/com.termux/cache")
        if termux_cache.exists():
            caches["termux"] = self._get_dir_size(termux_cache)
        
        # apt cache
        apt_cache = Path("/var/cache/apt")
        if apt_cache.exists():
            caches["apt"] = self._get_dir_size(apt_cache)
        
        # OWURA temp
        if self.temp_dir.exists():
            caches["owura_temp"] = self._get_dir_size(self.temp_dir)
        
        # Build artifacts
        build_dirs = list(self.home.rglob("build"))
        build_size = sum(self._get_dir_size(d) for d in build_dirs[:5])
        caches["builds"] = build_size
        
        # __pycache__
        pycache_dirs = list(self.home.rglob("__pycache__"))
        pycache_size = sum(self._get_dir_size(d) for d in pycache_dirs[:10])
        caches["pycache"] = pycache_size
        
        return caches
    
    def _get_dir_size(self, path: Path) -> int:
        """Get directory size in bytes."""
        try:
            total = 0
            for item in path.rglob("*"):
                if item.is_file():
                    total += item.stat().st_size
            return total
        except:
            return 0
    
    def _format_size(self, size_bytes: int) -> str:
        """Format bytes to human readable."""
        if size_bytes < 1024:
            return f"{size_bytes}B"
        elif size_bytes < 1024**2:
            return f"{size_bytes/1024:.1f}KB"
        elif size_bytes < 1024**3:
            return f"{size_bytes/1024**2:.1f}MB"
        else:
            return f"{size_bytes/1024**3:.2f}GB"
    
    def cleanup_pip(self) -> int:
        """Clean pip cache."""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "cache", "purge"],
                capture_output=True, text=True, timeout=30
            )
            self.log("Pip cache purged")
            return 1
        except:
            # Manual cleanup
            pip_cache = self.home / ".cache" / "pip"
            if pip_cache.exists():
                size = self._get_dir_size(pip_cache)
                shutil.rmtree(pip_cache, ignore_errors=True)
                self.log(f"Manually cleaned pip cache: {self._format_size(size)}")
                return size
            return 0
    
    def cleanup_npm(self) -> int:
        """Clean npm cache."""
        try:
            result = subprocess.run(
                ["npm", "cache", "clean", "--force"],
                capture_output=True, text=True, timeout=30
            )
            self.log("NPM cache cleaned")
            return 1
        except:
            npm_cache = self.home / ".npm"
            if npm_cache.exists():
                size = self._get_dir_size(npm_cache)
                shutil.rmtree(npm_cache, ignore_errors=True)
                self.log(f"Manually cleaned npm cache: {self._format_size(size)}")
                return size
            return 0
    
    def cleanup_apt(self) -> int:
        """Clean apt/package manager cache."""
        try:
            subprocess.run(["pkg", "clean", "-y"], capture_output=True, timeout=30)
            subprocess.run(["pkg", "autoclean", "-y"], capture_output=True, timeout=30)
            self.log("APT cache cleaned")
            return 1
        except:
            return 0
    
    def cleanup_temp(self) -> int:
        """Clean temporary files."""
        total_cleaned = 0
        
        # Clean /tmp
        temp_dirs = [Path("/tmp"), self.temp_dir]
        for temp in temp_dirs:
            if temp.exists():
                for item in temp.iterdir():
                    try:
                        if item.is_file():
                            size = item.stat().st_size
                            item.unlink()
                            total_cleaned += size
                        elif item.is_dir() and item.name.startswith("owura"):
                            size = self._get_dir_size(item)
                            shutil.rmtree(item, ignore_errors=True)
                            total_cleaned += size
                    except:
                        pass
        
        # Clean old log files
        log_dir = self.home / ".owura"
        if log_dir.exists():
            for log_file in log_dir.glob("*.log"):
                try:
                    # Keep logs smaller than 1MB
                    if log_file.stat().st_size > 1024 * 1024:
                        size = log_file.stat().st_size
                        log_file.write_text("")
                        total_cleaned += size
                except:
                    pass
        
        self.log(f"Cleaned temp files: {self._format_size(total_cleaned)}")
        return total_cleaned
    
    def cleanup_pycache(self) -> int:
        """Clean Python __pycache__ directories."""
        total_cleaned = 0
        
        for pycache in self.home.rglob("__pycache__"):
            try:
                size = self._get_dir_size(pycache)
                shutil.rmtree(pycache, ignore_errors=True)
                total_cleaned += size
            except:
                pass
        
        self.log(f"Cleaned __pycache__: {self._format_size(total_cleaned)}")
        return total_cleaned
    
    def cleanup_build_artifacts(self) -> int:
        """Clean build directories."""
        total_cleaned = 0
        
        # Common build directories
        build_patterns = ["build", "dist", "*.egg-info", ".cache"]
        
        for pattern in build_patterns:
            for item in self.home.rglob(pattern):
                if item.is_dir() and "node_modules" not in str(item):
                    try:
                        size = self._get_dir_size(item)
                        if size > 1024 * 1024:  # Only clean if > 1MB
                            shutil.rmtree(item, ignore_errors=True)
                            total_cleaned += size
                    except:
                        pass
        
        self.log(f"Cleaned build artifacts: {self._format_size(total_cleaned)}")
        return total_cleaned
    
    def full_compaction(self) -> dict:
        """Run full compaction and return stats."""
        self.log("Starting full compaction...")
        
        # Get before stats
        before_disk = self.get_disk_usage()
        before_memory = self.get_memory_usage()
        before_caches = self.get_cache_sizes()
        
        # Run cleanup
        cleaned = {
            "pip": self.cleanup_pip(),
            "npm": self.cleanup_npm(),
            "apt": self.cleanup_apt(),
            "temp": self.cleanup_temp(),
            "pycache": self.cleanup_pycache(),
            "builds": self.cleanup_build_artifacts(),
        }
        
        # Get after stats
        after_disk = self.get_disk_usage()
        after_memory = self.get_memory_usage()
        
        # Calculate freed space
        disk_freed = before_disk["used_gb"] - after_disk["used_gb"]
        
        self.log(f"Compaction complete. Freed {disk_freed:.2f}GB disk space")
        
        return {
            "disk_before": before_disk,
            "disk_after": after_disk,
            "memory_before": before_memory,
            "memory_after": after_memory,
            "disk_freed_gb": round(disk_freed, 2),
            "cache_sizes": before_caches,
            "cleaned": cleaned
        }
    
    def auto_compact(self, threshold_percent: float = 85.0) -> bool:
        """Auto-compact if usage is above threshold."""
        disk = self.get_disk_usage()
        memory = self.get_memory_usage()
        
        should_compact = False
        reasons = []
        
        if disk["percent_used"] > threshold_percent:
            should_compact = True
            reasons.append(f"Disk at {disk['percent_used']}%")
        
        if memory["percent_used"] > 90:
            should_compact = True
            reasons.append(f"Memory at {memory['percent_used']}%")
        
        if should_compact:
            self.log(f"Auto-compact triggered: {', '.join(reasons)}")
            self.full_compaction()
            return True
        
        return False
    
    def get_status(self) -> str:
        """Get formatted status report."""
        disk = self.get_disk_usage()
        memory = self.get_memory_usage()
        caches = self.get_cache_sizes()
        
        lines = [
            "## System Status",
            "",
            "### Disk",
            f"- Total: {disk['total_gb']}GB",
            f"- Used: {disk['used_gb']}GB ({disk['percent_used']}%)",
            f"- Free: {disk['free_gb']}GB",
            "",
            "### Memory",
            f"- Total: {memory['total_mb']}MB",
            f"- Used: {memory['used_mb']}MB ({memory['percent_used']}%)",
            f"- Available: {memory['available_mb']}MB",
            "",
            "### Cache Sizes",
        ]
        
        for name, size in sorted(caches.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"- {name}: {self._format_size(size)}")
        
        total_cache = sum(caches.values())
        lines.append(f"- **Total**: {self._format_size(total_cache)}")
        
        return "\n".join(lines)

# Global instance
_compactor = None

def get_compactor() -> Compactor:
    global _compactor
    if _compactor is None:
        _compactor = Compactor()
    return _compactor
