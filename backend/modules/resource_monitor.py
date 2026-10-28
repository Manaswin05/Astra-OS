"""
resource_monitor.py
Real-time CPU, RAM, Disk, and GPU monitoring with AI-driven optimization
recommendations.
"""

from fastapi import APIRouter
import psutil

try:
    import GPUtil  # optional — graceful fallback if not installed
    _GPU_AVAILABLE = True
except ImportError:
    _GPU_AVAILABLE = False

router = APIRouter(prefix="/resources", tags=["Resource Monitor"])


def _gpu_stats() -> list:
    """Return GPU stats if GPUtil is available, otherwise an empty list."""
    if not _GPU_AVAILABLE:
        return []
    gpus = GPUtil.getGPUs()
    return [
        {
            "id": g.id,
            "name": g.name,
            "load_percent": round(g.load * 100, 1),
            "memory_used_mb": round(g.memoryUsed, 1),
            "memory_total_mb": round(g.memoryTotal, 1),
            "memory_percent": round(g.memoryUtil * 100, 1),
            "temperature_c": g.temperature,
        }
        for g in gpus
    ]


@router.get("/status", summary="Full system resource snapshot")
def get_status():
    """Return a complete snapshot of CPU, RAM, Disk, GPU, and battery."""
    cpu_percent = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    battery = None
    bat = psutil.sensors_battery()
    if bat:
        battery = {
            "percent": bat.percent,
            "plugged_in": bat.power_plugged,
            "seconds_left": bat.secsleft if bat.secsleft != psutil.POWER_TIME_UNLIMITED else None,
        }

    return {
        "cpu": {
            "percent": cpu_percent,
            "core_count_logical": psutil.cpu_count(logical=True),
            "core_count_physical": psutil.cpu_count(logical=False),
        },
        "ram": {
            "total_gb": round(ram.total / 1e9, 2),
            "used_gb": round(ram.used / 1e9, 2),
            "free_gb": round(ram.available / 1e9, 2),
            "percent": ram.percent,
        },
        "disk": {
            "total_gb": round(disk.total / 1e9, 2),
            "used_gb": round(disk.used / 1e9, 2),
            "free_gb": round(disk.free / 1e9, 2),
            "percent": disk.percent,
        },
        "gpu": _gpu_stats() if _GPU_AVAILABLE else {"status": "unavailable"},
        "battery": battery,
    }


@router.get("/cpu", summary="Per-core CPU usage")
def get_cpu():
    """Return per-core CPU usage percentages."""
    per_core = psutil.cpu_percent(interval=0.5, percpu=True)
    return {
        "overall_percent": psutil.cpu_percent(interval=0),
        "per_core": [{"core": i, "percent": p} for i, p in enumerate(per_core)],
        "frequency_mhz": psutil.cpu_freq().current if psutil.cpu_freq() else None,
    }


@router.get("/optimize", summary="AI optimization recommendations")
def get_recommendations():
    """
    Analyze current resource usage and return actionable recommendations.
    Uses simple threshold-based rules — no external model required.
    """
    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    recommendations = []
    priority = "low"

    # CPU recommendations
    if cpu > 90:
        recommendations.append({
            "resource": "CPU",
            "current_usage": f"{cpu}%",
            "recommendation": "CPU critically overloaded. Terminate non-essential background processes immediately.",
            "action": "kill_background_processes",
        })
        priority = "critical"
    elif cpu > 80:
        recommendations.append({
            "resource": "CPU",
            "current_usage": f"{cpu}%",
            "recommendation": "High CPU usage detected. Reduce background processes and defer non-urgent tasks.",
            "action": "reduce_background_processes",
        })
        priority = "high"
    elif cpu > 60:
        recommendations.append({
            "resource": "CPU",
            "current_usage": f"{cpu}%",
            "recommendation": "Moderate CPU load. Consider pausing browser tabs or heavy desktop apps.",
            "action": "pause_non_critical_apps",
        })
        priority = max(priority, "medium") if priority == "low" else priority

    # RAM recommendations
    if ram.percent > 90:
        recommendations.append({
            "resource": "RAM",
            "current_usage": f"{ram.percent}%",
            "recommendation": "Memory critically low. Clear system cache and close unused applications.",
            "action": "clear_cache_and_close_apps",
        })
        priority = "critical"
    elif ram.percent > 80:
        recommendations.append({
            "resource": "RAM",
            "current_usage": f"{ram.percent}%",
            "recommendation": "High memory usage. Clear cache or close unused applications.",
            "action": "clear_cache",
        })
        priority = "high" if priority != "critical" else priority

    # Disk recommendations
    if disk.percent > 90:
        recommendations.append({
            "resource": "Disk",
            "current_usage": f"{disk.percent}%",
            "recommendation": "Disk nearly full. Delete temporary files and move large files to external storage.",
            "action": "cleanup_disk",
        })

    if not recommendations:
        recommendations.append({
            "resource": "All",
            "current_usage": "Normal",
            "recommendation": "System resources are healthy. No action needed.",
            "action": "none",
        })
        priority = "low"

    return {
        "priority": priority,
        "cpu_percent": cpu,
        "ram_percent": ram.percent,
        "disk_percent": disk.percent,
        "recommendations": recommendations,
    }
